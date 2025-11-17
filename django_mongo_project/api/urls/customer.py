# api/urls.py
from django.urls import path
from api.views.customer import *

urlpatterns = [
    path('register/', api_register, name='api-register'),
    path('login/', api_login, name='api-login'),
    path('logout/', api_logout, name='api-logout'),

    path('get_customer/<str:customer_id>/', get_customer, name='get_customer'),
    path('up_date/<str:customer_id>/', update_customer, name='update_customer'),
]