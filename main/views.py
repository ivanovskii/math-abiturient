from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    return render(request, 'main/index.html')


@login_required
def profile(request):
    return render(request, 'main/profile.html')


class MALoginView(LoginView):
    template_name = 'main/login.html'


class MALogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'
