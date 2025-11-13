# your_app/urls.py

from django.urls import path
from api.views.review import *

urlpatterns = [    
    path('get_by_id/<str:product_id>/', get_reviews_by_product_id, name='get_reviews_by_product_id'),
    path('add/', add_review_insecure, name='add_review_insecure'),
    path('<str:review_id>/delete/', delete_review, name='delete_review'), 
]
