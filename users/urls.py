from django.contrib.auth import views as auth_views
from django.urls import path

from users import views as users_views

urlpatterns = [
    path('register/', users_views.register, name='register'),
    path('profile/', users_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/request/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset/request.html'),
         name='password_reset_request'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset/done.html'),
         name='password_reset_done'),

    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset/complete.html'),
         name='password_reset_complete'),

    path('password-reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset/confirm.html'),
         name='password_reset_confirm'),

]
