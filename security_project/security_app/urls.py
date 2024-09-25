from django.urls import path
from .views import *

# password reset 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('dashboard/',dashboard,name='dashboard'),
    path('user-logout/',user_logout,name='user-logout'),
    path('account-locked/',account_locked,name='account-locked'),
    
    # password reset 
    # email submit form
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='password_reset/password-reset.html'),name='reset_password'),
    # Reset message
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password-reset-sent.html'),name='password_reset_done'),
    # Link for password reset
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password-reset-form.html'),name='password_reset_confirm'),
    # Password changed success message
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password-reset-complete.html'),name='password_reset_complete'),
    
]