from django.urls import path
from api.views.customer_admin import (
    get_all_customers,
    delete_customer,
    get_customer_statistics
)

urlpatterns = [
    path('', get_all_customers, name='get_all_customers'),
    path('statistics/', get_customer_statistics, name='get_customer_statistics'),
    path('<str:customer_id>/delete/', delete_customer, name='delete_customer'),
]
