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

@api_view(['DELETE'])
def delete_review(request, review_id):
    """
    API endpoint để xóa một bài đánh giá.
    CẢNH BÁO: API này không yêu cầu xác thực. Bất kỳ ai cũng có thể xóa.
    Chỉ nên dùng cho mục đích phát triển.
    """
    try:
        # 1. Tìm bài đánh giá cần xóa
        logger.info(f"Đang cố gắng xóa review với ID: {review_id}")
        review = Review.objects.get(id=review_id)
        logger.info(f"Tìm thấy review: {review.id}")

        # 2. Xóa luôn, không kiểm tra quyền
        review.delete()
        logger.info(f"Đã xóa thành công review {review.id}")

        return Response(
            {"message": "Xóa bài đánh giá thành công."},
            status=status.HTTP_200_OK
        )

    except DoesNotExist:
        logger.error(f"Không tìm thấy review với ID: {review_id}")
        return Response(
            {"error": "Không tìm thấy bài đánh giá."},
            status=status.HTTP_404_NOT_FOUND
        )
    except (InvalidId, ValueError) as e:
        logger.error(f"ID review không hợp lệ: {review_id}. Lỗi: {e}")
        return Response(
            {"error": "ID bài đánh giá không hợp lệ."},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.exception(f"Lỗi không xác định trong delete_review: {e}")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
