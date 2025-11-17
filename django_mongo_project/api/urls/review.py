# api/urls/review.py

from django.urls import path
from api.views.review import (
    get_reviews_by_product_id, 
    add_review_insecure
)
# Import view công khai mới
from api.views.admin_response import get_public_admin_responses

urlpatterns = [    
    path('get_by_id/<str:product_id>/', get_reviews_by_product_id, name='get_reviews_by_product_id'),
    path('add/', add_review_insecure, name='add_review_insecure'),
    
    # --- THÊM ĐƯỜNG DẪN CÔNG KHAI NÀY ---
    path('<str:review_id>/responses/', get_public_admin_responses, name='get_public_admin_responses'),
]