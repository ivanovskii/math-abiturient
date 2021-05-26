from django.urls import path
from .views import (
    index, profile, MALoginView, MALogoutView,
    ChangeUserInfoView, MAPasswordChangeView,
    RegisterUserView, RegisterDoneView,
    user_activate,
)

urlpatterns = [
    path('accounts/login/', MALoginView.as_view(), name='login'),
    path('accounts/logout/', MALogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(),
                                     name='profile_change'),
    path('accounts/password/change/', MAPasswordChangeView.as_view(),
                                      name='password_change'),
    path('accounts/register/done/', RegisterDoneView.as_view(),
                                   name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(),
                                   name='register'),
    path('accounts/register/activate/<str:sign>/', user_activate,
                                   name='register_activate'),
    path('', index, name='index'),
]
