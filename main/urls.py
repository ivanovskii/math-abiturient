from django.urls import path

from .views import index, UserLoginView, UserDetailView, UserLogoutView, \
    EditProfileView, PasswordChangeView, JoinView, \
    JoinDoneView, user_activate, DeleteUserView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView


urlpatterns = [
    path('', index, name='index'),

    # Авторизация и выход
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Регистрация нового пользователя
    path('join/', JoinView.as_view(), name='join'),
    path('join/done/', JoinDoneView.as_view(), name='join_done'),
    path('join/activate/<str:sign>/', user_activate, name='join_activate'),

    # Настройка пользователя
    path('edit/', EditProfileView.as_view(), name='edit_profile'),
    path('password/change/', PasswordChangeView.as_view(),
                                            name='password_change'),
    path('delete', DeleteUserView.as_view(),
                                   name='profile_delete'),
    
    # Cброс пароля
    path('password/reset/', PasswordResetView.as_view(),
                            name='password_reset'),
    path('password/reset/done/', PasswordResetDoneView.as_view(),
                                 name='password_reset_done'),
    path('password/confirm/<uidb64>/<token>/',
                                    PasswordResetConfirmView.as_view(),
                                    name='password_reset_confirm'),
    path('password/confirm/complete/',
                                    PasswordResetCompleteView.as_view(),
                                    name='password_reset_complete'),

    path('<str:username>/', UserDetailView.as_view(), name='profile'),
]
