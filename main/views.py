from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView, \
    PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, CreateView, \
    DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.core.signing import BadSignature
from django.contrib.auth import logout
from django.contrib import messages

from .models import AdvUser
from .forms import EditProfileForm, JoinForm, LoginForm
from .utilities import signer


def index(request):
    return render(request, 'main/index.html')


##### Авторизация и выход

class UserLoginView(LoginView):
    template_name = 'main/login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse_lazy('profile', args=[self.request.user.username])


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/index.html'


##### Регистрация пользователя

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


##### Настройки пользователя

class EditProfileView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/edit_profile.html'
    form_class = EditProfileForm
    login_url = 'login'
    success_message = 'Данные пользователя изменены'
    
    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.username])

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args , **kwargs)

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
        return reverse_lazy('profile', args=[self.request.user.username])


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


##### Сброс пароля

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


# Просмотр профиля
class UserDetailView(DetailView):
    model = AdvUser
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "main/profile.html"