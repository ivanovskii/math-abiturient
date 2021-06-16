import json
from datetime import datetime

from django.core.signing import BadSignature
from django.core.exceptions import PermissionDenied
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView,
)

from .models import AdvUser, Task, FavoriteTask
from .forms import LoginForm, JoinForm, UpdateUserForm, CreateTaskForm
from .utilities import signer

class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(is_published=True)
        context['tasks'] = tasks
        if self.request.user.is_authenticated:
            context['user_favorites'] = Task.objects.filter(
                favoritetask__user=self.request.user)
        return context


class SearchView(View):
    template_name = 'main/search.html'

    def get(self, request, *args, **kwargs):
        context = {}

        question = request.GET.get('q')
        if question is not None:
            search_tasks = Task.objects.filter(title__contains=question, is_published=True)

            context['task_list'] = search_tasks
            if self.request.user.is_authenticated:
                context['user_favorites'] = Task.objects.filter(
                    favoritetask__user=self.request.user)

        return render(request, template_name=self.template_name, context=context)


##### Login and logout

class UserLoginView(LoginView):
    template_name = 'main/login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse_lazy('profile', args=[self.request.user.username])


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/index.html'
    login_url = 'login'


##### New User Registration

class JoinView(CreateView):
    model = AdvUser
    template_name = 'main/join.html'
    form_class = JoinForm
    success_url = reverse_lazy('join_done')


class JoinDoneView(TemplateView):
    template_name = 'main/join_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


##### Account settings

class UpdateUserView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/edit_profile.html'
    form_class = UpdateUserForm
    login_url = 'login'
    success_message = 'Данные пользователя изменены'
    
    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args , **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    login_url = 'login'
    success_url = reverse_lazy('index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class PasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                                              PasswordChangeView):
    template_name = 'main/password_change.html'
    success_message = 'Пароль успешно изменен'
    login_url = 'login'

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])


##### Password reset

class PasswordResetView(PasswordResetView):
    template_name = 'main/password_reset.html'
    subject_template_name = 'email/reset_letter_subject.txt'
    email_template_name = 'email/reset_letter_body.txt'
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'main/password_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'main/password_complete.html'


# Profile view
class UserDetailView(DetailView):
    model = AdvUser
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "main/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_favorites'] = Task.objects.filter(
                favoritetask__user=self.request.user)
        context['object_favorites'] = Task.objects.filter(
            favoritetask__user=context['object'])
        return context


#### Tasks

class CreateTaskView(LoginRequiredMixin, CreateView):
    form_class = CreateTaskForm
    template_name = 'task/create.html'
    login_url = 'login'

    def form_valid(self, form):
        """ Creator of task is request.user """
        form.instance.creator = self.request.user
        if self.request.POST.get("publish"):
            form.instance.published_at = datetime.now()
            form.instance.is_published = True
        return super(CreateTaskView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])


class ReadTaskView(DetailView):
    model = Task
    template_name = 'task/read.html'


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'task/update.html'
    form_class = CreateTaskForm
    login_url = 'login'
    
    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user """
        obj = super(UpdateTaskView, self).get_object()
        if not obj.creator == self.request.user:
            raise PermissionDenied
        return obj


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task/delete.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse('profile', args=[self.request.user.username])

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user """
        obj = super(DeleteTaskView, self).get_object()
        if not obj.creator == self.request.user:
            raise PermissionDenied
        return obj


class PublishTaskView(LoginRequiredMixin, View):
    model = Task
    login_url = "login"

    def get(self, request, pk):
        task = get_object_or_404(Task, id=pk)
        if request.user == task.creator:
            if task.is_published:
                task.published_at = None
                task.is_published = False
                FavoriteTask.objects.filter(obj__pk=task.pk).delete() 
            else:
                task.published_at = datetime.now()
                task.is_published = True
            task.save()
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
        else:
            raise PermissionDenied


class FavoriteTaskView(View):
    model = None
    login_url = "login"

    def post(self, request, pk):
        user = auth.get_user(request)
        if user.is_anonymous:
            raise PermissionDenied
        favorite, created = self.model.objects.get_or_create(user=user, obj_id=pk)
        if not created:
            favorite.delete()
 
        return HttpResponse(
            json.dumps({
                "result": created,
                # "count": self.model.objects.filter(obj_id=pk).count()
            }),
            content_type="application/json"
        )
