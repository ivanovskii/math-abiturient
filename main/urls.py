from django.urls import path

from .views import (
    index, profile,
    MALoginView, MALogoutView
)

urlpatterns = [
    path('accounts/login/', MALoginView.as_view(), name='login'),
    path('accounts/logout/', MALogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('', index, name='index'),
]