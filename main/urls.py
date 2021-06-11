from django.urls import path

from .views import index, UserLoginView, UserDetailView, UserLogoutView, \
    EditProfileView, PasswordChangeView, JoinView, \
    JoinDoneView, user_activate, DeleteUserView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, CreateTaskView, ShowTaskView


urlpatterns = [
    path('', index, name='index'),
    
    # Task CRUD
    path('task/create/', CreateTaskView.as_view(), name='create_task'),
    path('task/<int:pk>/', ReadTaskView.as_view(), name='read_task'),
    path('task/<int:pk>/update/', UpdateTaskView.as_view(), name='update_task'),
    path('task/<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_task'),

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
