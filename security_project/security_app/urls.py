from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('dashboard/',dashboard,name='dashboard'),
    path('user-logout/',user_logout,name='user-logout'),
    path('account-locked/',account_locked,name='account-locked'),
]