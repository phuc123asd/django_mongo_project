# api/urls/review_admin.py

from django.urls import path
from api.views.review_admin import (
    get_all_reviews,
    delete_review,
    get_review_statistics
)
# Import các view cho admin response
from api.views.admin_response import (
    get_admin_responses,
    add_admin_response,
    generate_ai_response,
    update_admin_response,
    delete_admin_response
)

# Các URL quản lý review cũ
urlpatterns = [
    path('', get_all_reviews, name='get_all_reviews'),
    path('statistics/', get_review_statistics, name='get_review_statistics'),
    path('<str:review_id>/delete/', delete_review, name='delete_review'),
]

# --- THÊM CÁC ĐƯỜNG DẪN QUẢN LÝ PHẢN HỒI ---
urlpatterns += [
    # Lấy (dành cho admin)
    path('admin-responses/<str:review_id>/', get_admin_responses, name='get_admin_responses'),
    # Thêm
    path('admin-responses/add/', add_admin_response, name='add_admin_response'),
    # Tạo AI
    path('admin-responses/generate/', generate_ai_response, name='generate_ai_response'),
    # Cập nhật
    path('admin-responses/update/<str:response_id>/', update_admin_response, name='update_admin_response'),
    # Xóa
    path('admin-responses/delete/<str:response_id>/', delete_admin_response, name='delete_admin_response'),
]