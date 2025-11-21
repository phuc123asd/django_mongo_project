# api/views/admin_response.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models.admin_response import AdminResponse
from api.serializers.admin_response import AdminResponseSerializer

from mongoengine.errors import DoesNotExist
import logging
from openai import OpenAI
from django.conf import settings

logger = logging.getLogger(__name__)

# Khởi tạo OpenAI client
openai_client = None
if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "placeholder":
    try:
        openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    except Exception as e:
        logger.warning(f"Could not initialize OpenAI client: {e}")

def generate_ai_response_text(review_rating, review_comment, product_name):
    """Hàm helper để tạo text phản hồi từ AI."""
    if not openai_client:
        if review_rating < 3:
            return "Chúng tôi rất tiếc khi bạn chưa hài lòng. Vui lòng liên hệ bộ phận CSKH để được hỗ trợ tốt hơn."
        else:
            return "Cảm ơn bạn đã đánh giá tích cực! Chúng tôi rất vui khi bạn hài lòng."
    
    try:
        prompt = f"""Bạn là đại diện CSKH. Một khách hàng đánh giá {review_rating} sao cho sản phẩm "{product_name}" với bình luận: "{review_comment}". Hãy viết một phản hồi ngắn gọn (2-3 câu), thân thiện và chuyên nghiệp. Chỉ trả về nội dung phản hồi."""
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return "Cảm ơn bạn đã đánh giá. Phản hồi tự động đang gặp sự cố."

# --- VIEW CÔNG KHAI (KHÔNG YÊU CẦU ĐĂNG NHẬP) ---
@api_view(['GET'])
def get_public_admin_responses(request, review_id):
    """Lấy tất cả phản hồi cho một review (công khai cho mọi người)."""
    try:
        responses = AdminResponse.objects.filter(review_id=review_id).order_by('created_at')
        serializer = AdminResponseSerializer(responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching public admin responses: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- CÁC VIEW DÀNH CHO ADMIN (YÊU CẦU ĐĂNG NHẬP) ---
@api_view(['GET'])
def get_admin_responses(request, review_id):
    """Lấy tất cả phản hồi cho một review (admin only)."""
    try:
        responses = AdminResponse.objects.filter(review_id=review_id).order_by('-created_at')
        serializer = AdminResponseSerializer(responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching admin responses: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])

def add_admin_response(request):
    """Thêm một phản hồi mới từ admin."""
    try:
        data = request.data
        data['admin_id'] = request.session.get('admin_id', 'unknown')
        data['admin_name'] = request.session.get('admin_name', 'Admin')
        data['response_type'] = 'manual'
        
        serializer = AdminResponseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error adding admin response: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def generate_ai_response(request):
    """Tạo và lưu một phản hồi tự động bằng AI."""
    try:
        review_id = request.data.get('review_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        product_name = request.data.get('product_name', 'sản phẩm')
        
        if not all([review_id, rating, comment]):
            return Response({"error": "Thiếu thông tin review_id, rating, hoặc comment"}, status=status.HTTP_400_BAD_REQUEST)
        
        ai_text = generate_ai_response_text(rating, comment, product_name)
        
        data = {
            'review_id': review_id,
            'response': ai_text,
            'admin_id': 'ai-assistant',
            'admin_name': 'AI Assistant',
            'response_type': 'ai'
        }
        
        serializer = AdminResponseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error generating AI response: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_admin_response(request, response_id):
    """Cập nhật một phản hồi."""
    try:
        response_obj = AdminResponse.objects.get(id=response_id)
        response_obj.response = request.data.get('response')
        response_obj.response_type = 'manual' # Đánh dấu là đã chỉnh sửa thủ công
        response_obj.save()
        
        serializer = AdminResponseSerializer(response_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except DoesNotExist:
        return Response({"error": "Không tìm thấy phản hồi."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error updating admin response: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_admin_response(request, response_id):
    """Xóa một phản hồi."""
    try:
        response_obj = AdminResponse.objects.get(id=response_id)
        response_obj.delete()
        return Response({"message": "Đã xóa phản hồi thành công."}, status=status.HTTP_200_OK)
    except DoesNotExist:
        return Response({"error": "Không tìm thấy phản hồi."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error deleting admin response: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)