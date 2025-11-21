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


# --- THÊM 2 IMPORT NÀY ---
from api.models.admin_response import AdminResponse
from api.serializers.admin_response import AdminResponseSerializer

from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import NotFound
import logging

# Cấu hình logging để in ra console
logger = logging.getLogger(__name__)

from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_ai_response_text(rating, comment, product_name):
    try:
        prompt = f"""
Bạn là nhân viên chăm sóc khách hàng. Hãy viết một phản hồi phù hợp cho đánh giá sản phẩm.

Thông tin đánh giá:
- Tên sản phẩm: {product_name}
- Số sao: {rating}/5
- Nội dung khách hàng viết: "{comment}"

Yêu cầu khi phản hồi:
- Viết ngắn gọn 1–3 câu.
- Giọng văn tự nhiên, thân thiện, chuyên nghiệp.
- Nội dung phải đa dạng, không lặp lại khuôn mẫu.
- Phản hồi dựa theo số sao:

1 sao:
- Xin lỗi chân thành.
- Hỏi thêm thông tin hoặc đề nghị hỗ trợ.
- Giữ thái độ chân thành và thiện chí.

2 sao:
- Gửi lời xin lỗi nhẹ nhàng.
- Thừa nhận trải nghiệm chưa tốt.
- Cam kết cải thiện và mong khách chia sẻ thêm.

3 sao:
- Trung lập và chuyên nghiệp.
- Cảm ơn vì góp ý.
- Thể hiện mong muốn cải thiện thêm.

4 sao:
- Cảm ơn tích cực.
- Ghi nhận góp ý (nếu có).
- Thể hiện sẽ cố gắng để tốt hơn.

5 sao:
- Cảm ơn vui vẻ và nồng nhiệt.
- Thể hiện sự trân trọng.
- Chúc khách có trải nghiệm tuyệt vời hơn.

Viết phản hồi ngay bây giờ.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là nhân viên CSKH chuyên nghiệp."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content

    except Exception as e:
        return "Cảm ơn bạn đã đánh giá! Chúng tôi sẽ ghi nhận để cải thiện tốt hơn."

@api_view(['GET'])
def get_reviews_by_product_id(request, product_id):
    try:
        reviews = Review.objects.filter(product_id=product_id).order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- 1. API Thêm Đánh Giá Mới (Phiên bản an toàn) ---
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    try:
        customer = request.user
        data = request.data
        data['customer_id'] = str(customer.id) # Đảm bảo customer_id là string

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            # Chỉ lưu review, không tạo phản hồi tự động
            review = serializer.save()
            
            logger.info(f"Review created by user {customer.id} for product {review.product_id}")
            
            # Trả về data của review vừa tạo
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error in add_review: {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- 2. API Thêm Đánh Giá Mới (Phiên bản không an toàn) ---
# CẢNH BÁO: Bất kỳ ai cũng có thể đăng đánh giá
# api/views/review.py

@api_view(['POST'])
def add_review_insecure(request):
    try:
        data = request.data
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            # 1. Lưu review trước
            review = serializer.save()
            logger.info(f"Review created insecurely for product {review.product_id}")
            
            # 2. --- BẮT ĐẦU ĐOẠN TỰ ĐỘNG TẠO PHẢN HỒI ---
            try:
                # Gọi hàm tạo nội dung phản hồi từ AI
                # Bạn có thể truyền thêm tên sản phẩm nếu có
                ai_text = generate_ai_response_text(review.rating, review.comment, "sản phẩm")
                
                # Tạo và lưu một AdminResponse mới vào database
                AdminResponse.objects.create(
                    review_id=str(review.id),  # Liên kết với review vừa tạo
                    response=ai_text,
                    admin_id='ai-assistant',
                    admin_name='AI Assistant',
                    response_type='ai'
                )
                logger.info(f"AI response auto-generated for review {review.id}")
            except Exception as ai_err:
                # Nếu có lỗi trong quá trình tạo AI, chỉ log lỗi chứ không làm hỏng việc tạo review
                logger.error(f"Failed to auto-generate AI response for review {review.id}: {ai_err}")
            # 3. --- KẾT THÚC ĐOẠN TỰ ĐỘNG TẠO PHẢN HỒI ---

            # Trả về data của review vừa tạo
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error in add_review_insecure: {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)