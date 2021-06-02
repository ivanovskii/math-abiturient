from django.urls import path

from .views import index, MALoginView, UserDetailView, MALogoutView, \
    ChangeUserInfoView, MAPasswordChangeView, JoinUserView, \
    JoinDoneView, user_activate, DeleteUserView, MAPasswordResetView, \
    MAPasswordResetDoneView, MAPasswordResetConfirmView, \
    MAPasswordResetCompleteView


urlpatterns = [
    path('login/', MALoginView.as_view(), name='login'),
    path('logout/', MALogoutView.as_view(), name='logout'),
    path('<str:username>/change/', ChangeUserInfoView.as_view(),
                                     name='profile_change'),
    path('<str:username>/password/change/', MAPasswordChangeView.as_view(),
                                      name='password_change'),
    path('join/done/', JoinDoneView.as_view(),
                                   name='join_done'),
    path('join/', JoinUserView.as_view(),
                                   name='join'),
    path('join/activate/<str:sign>/', user_activate,
                                   name='join_activate'),
    path('<str:username>/delete', DeleteUserView.as_view(),
                                   name='profile_delete'),
    path('password/reset/done/', MAPasswordResetDoneView.as_view(),
                                          name='password_reset_done'),
    path('password/reset/', MAPasswordResetView.as_view(),
                                     name='password_reset'),
    path('password/confirm/complete/',
                                    MAPasswordResetCompleteView.as_view(),
                                    name='password_reset_complete'),
    path('password/confirm/<uidb64>/<token>/',
                                    MAPasswordResetConfirmView.as_view(),
                                    name='password_reset_confirm'),
    path('<str:username>/', UserDetailView.as_view(), name='profile'),
    path('', index, name='index'),
]
