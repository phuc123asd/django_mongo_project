# api/views/review.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from mongoengine.errors import DoesNotExist, ValidationError
from bson.errors import InvalidId
from api.models.review import Review
from api.serializers.review import ReviewSerializer
from api.models.customer import Customer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import NotFound # <-- THÊM IMPORT NÀY
import logging

# Cấu hình logging để in ra console
logger = logging.getLogger(__name__)

# api/views/review.py

@api_view(['GET'])
def get_reviews_by_product_id(request, product_id):
    try:
        # Lọc theo trường product_id mới
        reviews = Review.objects.filter(product_id=product_id).order_by('-created_at')
        
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ... các view khác của bạn ...

# --- 3. API Thêm Đánh Giá Mới ---
# Phiên bản an toàn (Khuyến nghị)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    try:
        # Lấy thông tin khách hàng từ request (đã được xác thực)
        customer = request.user  # Giả sử bạn dùng Django's authentication framework

        data = request.data
        data['customer'] = customer.id # Gán customer từ session vào data

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Phiên bản không an toàn (Hoạt động ngay với frontend hiện tại)
# CẢNH BẢO: Bất kỳ ai cũng có thể đăng đánh giá
@api_view(['POST'])
# @permission_classes([IsAuthenticated]) # <-- Bỏ comment này
def add_review_insecure(request):
    try:
        data = request.data
        # Frontend gửi customer_id, ta tin tưởng vào nó (KHÔNG AN TOÀN)
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
