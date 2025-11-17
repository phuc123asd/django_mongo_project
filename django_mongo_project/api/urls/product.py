from django.urls import path
from api.views.product import (
    product_list, 
    product_detail,
    product_create,
    product_update,
    product_delete
)

urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', product_create, name='product_create'),
    path('<str:product_id>/', product_detail, name='product_detail'),
    path('<str:product_id>/update/', product_update, name='product_update'),
    path('<str:product_id>/delete/', product_delete, name='product_delete'),
]
