# api/urls.py
from django.urls import path
from api.views.order import *
from api.views.momo import create_momo_payment, momo_ipn, get_payment_status, confirm_momo_payment

urlpatterns = [
    path('create/', create_order, name='create_order'), 
    path('customer/<str:customer_id>/', get_orders_by_customer, name='get_orders_by_customer'),
    path('<str:order_id>/status/', update_order_status, name='update_order_status'),
    path('<str:order_id>/', get_order_detail, name='get_order_detail'),
    path('', get_all_orders, name='get_all_orders'),
    # MoMo payment
    path('momo/create-payment/', create_momo_payment, name='create_momo_payment'),
    path('momo/confirm-payment/', confirm_momo_payment, name='confirm_momo_payment'),
    path('momo/ipn/', momo_ipn, name='momo_ipn'),
    path('momo/payment-status/<str:order_id>/', get_payment_status, name='get_payment_status'),
]
