# api/urls.py
from django.urls import path
from api.views.order import *

urlpatterns = [
    path('create/', create_order, name='create_order'), 
    path('customer/<str:customer_id>/', get_orders_by_customer, name='get_orders_by_customer'),
    path('<str:order_id>/', get_order_detail, name='get_order_detail'),
    path('', get_all_orders, name='get_all_orders'),
]
