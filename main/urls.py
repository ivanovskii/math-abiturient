from django.urls import path

from .views import index, MALoginView, profile, MALogoutView, \
    ChangeUserInfoView, MAPasswordChangeView, RegisterUserView, \
    RegisterDoneView, user_activate, DeleteUserView, MAPasswordResetView, \
    MAPasswordResetDoneView, MAPasswordResetConfirmView, \
    MAPasswordResetCompleteView


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
    path('accounts/profile/delete', DeleteUserView.as_view(),
                                   name='profile_delete'),
    path('accounts/password/reset/done/', MAPasswordResetDoneView.as_view(),
                                          name='password_reset_done'),
    path('accounts/password/reset/', MAPasswordResetView.as_view(),
                                     name='password_reset'),
    path('accounts/password/confirm/complete/',
                                    MAPasswordResetCompleteView.as_view(),
                                    name='password_reset_complete'),
    path('accounts/password/confirm/<uidb64>/<token>/',
                                    MAPasswordResetConfirmView.as_view(),
                                    name='password_reset_confirm'),
    path('', index, name='index'),
]
