from django.urls import path
from api.views import admin_auth

urlpatterns = [
    path('register/', admin_auth.admin_register, name='admin-register'),
    path('login/', admin_auth.admin_login, name='admin-login'),
    path('logout/', admin_auth.admin_logout, name='admin-logout'),
    path('me/', admin_auth.admin_me, name='admin-me'),
]
