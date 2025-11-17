# api/urls.py
from django.urls import path
from api.views.order import (
    create_order,
    get_orders_by_customer,
    get_order_detail,
    get_all_orders,
    update_order_status,
    delete_order,
    get_order_statistics
)

urlpatterns = [
    path('', get_all_orders, name='get_all_orders'),
    path('statistics/', get_order_statistics, name='get_order_statistics'),
    path('create/', create_order, name='create_order'), 
    path('customer/<str:customer_id>/', get_orders_by_customer, name='get_orders_by_customer'),
    path('<str:order_id>/', get_order_detail, name='get_order_detail'),
    path('<str:order_id>/update-status/', update_order_status, name='update_order_status'),
    path('<str:order_id>/delete/', delete_order, name='delete_order'),
]
