# api/views/review_response.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.serializers.review_response import ReviewResponseSerializer

@api_view(['POST'])
def create_review_response(request):
    """
    Function-based API View để tạo một phản hồi mới cho một đánh giá.
    KHÔNG YÊU CẦU XÁC THỰC - Chỉ dùng cho phát triển hoặc kiểm thử.
    Chỉ cho phép phương thức POST.
    """
    # 1. Khởi tạo serializer với dữ liệu từ request
    serializer = ReviewResponseSerializer(data=request.data)

    # 2. Kiểm tra xem dữ liệu có hợp lệ không
    if serializer.is_valid():
        # 3. Nếu hợp lệ, lưu đối tượng vào database
        serializer.save()
        
        # 4. Trả về dữ liệu vừa tạo với mã trạng thái 201 (Created)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # 5. Nếu dữ liệu không hợp lệ, trả về lỗi với mã trạng thái 400 (Bad Request)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)