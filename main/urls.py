from django.urls import path
from .views import (
    index, profile, MALoginView, MALogoutView,
    ChangeUserInfoView, MAPasswordChangeView,
)

urlpatterns = [
    path('accounts/login/', MALoginView.as_view(), name='login'),
    path('accounts/logout/', MALogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(),
                                     name='profile_change'),
    path('accounts/password/change/', MAPasswordChangeView.as_view(),
                                      name='password_change'),
    path('', index, name='index'),
]
