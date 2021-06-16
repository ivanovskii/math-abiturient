from django.urls import path

from .views import (
    index,
    CreateTaskView, ReadTaskView, UpdateTaskView, DeleteTaskView,
    UserLoginView, UserLogoutView,
    JoinView, JoinDoneView, user_activate,
    UpdateUserView, PasswordChangeView, DeleteUserView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    UserDetailView,
)


urlpatterns = [
    path('', index, name='index'),
    
    # Task CRUD
    path('task/create/', CreateTaskView.as_view(), name='create_task'),
    path('task/<int:pk>/', ReadTaskView.as_view(), name='read_task'),
    path('task/<int:pk>/update/', UpdateTaskView.as_view(), name='update_task'),
    path('task/<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_task'),

    # Login and Logout 
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # New User Registration
    path('join/', JoinView.as_view(), name='join'),
    path('join/done/', JoinDoneView.as_view(), name='join_done'),
    path('join/activate/<str:sign>/', user_activate, name='join_activate'),

    # Account settings
    path('account/update/', UpdateUserView.as_view(), name='edit_profile'),
    path('account/password/update/', PasswordChangeView.as_view(),
                                     name='password_change'),
    path('account/delete/', DeleteUserView.as_view(),
                            name='profile_delete'),
    
    # Password reset using email
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
