from django.shortcuts import render
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import AdvUser
from .forms import ChangeUserInfoForm


def index(request):
    return render(request, 'main/index.html')


@login_required
def profile(request):
    return render(request, 'main/profile.html')


class MALoginView(LoginView):
    template_name = 'main/login.html'


class MALogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args , **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class MAPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                                                PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = 'Пароль успешно изменен'
