# api/views/customer.py

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from api.models.customer import Customer
from api.serializers.customer import CustomerSerializer
from api.decorators.decorators import require_session_auth
from mongoengine.errors import DoesNotExist
from bson import ObjectId
import logging  # Để log

logger = logging.getLogger(__name__)

# --- REGISTER ---
@api_view(['POST'])
def api_register(request):
    """
    API đăng ký người dùng mới.
    Frontend mong đợi message: 'User registered successfully'
    """
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')

    if not email or not password:
        return Response({'error': 'Vui lòng cung cấp cả email và mật khẩu.'}, status=status.HTTP_400_BAD_REQUEST)

    if Customer.objects(email=email).first():
        return Response({'error': 'Email này đã được sử dụng.'}, status=status.HTTP_409_CONFLICT)

    try:
        customer = Customer(
            email=email,
            password=password, # Lưu trực tiếp, không mã hóa
            first_name=first_name,
            last_name=request.data.get('last_name', ''),
            phone=request.data.get('phone', ''),
            address=request.data.get('address', ''),
            city=request.data.get('city', ''),
            province=request.data.get('province', ''),
            postal_code=request.data.get('postal_code', ''),
        )
        customer.save()
        
        # Sau khi đăng ký, tự động đăng nhập user
        request.session['user_id'] = str(customer.id)
        request.session['user_email'] = customer.email

        return Response({
            'message': 'User registered successfully',  # <-- Message phải khớp chính xác
            'id': str(customer.id) # <-- Trả về ID để frontend fetch thông tin chi tiết
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': 'Đã có lỗi xảy ra.', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- LOGIN ---
@api_view(['POST'])
def api_login(request):
    """
    API đăng nhập.
    Frontend mong đợi message: 'Login successful'
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Vui lòng cung cấp cả email và mật khẩu.'}, status=status.HTTP_400_BAD_REQUEST)

    customer = Customer.objects(email=email).first()
    
    # So sánh mật khẩu dạng văn bản thuần
    if not customer or password != customer.password:
        return Response({'error': 'Email hoặc mật khẩu không chính xác.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Lưu thông tin vào session
    request.session['user_id'] = str(customer.id)
    request.session['user_email'] = customer.email
    
    return Response({
        'message': 'Login successful', # <-- Message phải khớp chính xác
        'id': str(customer.id), # <-- Trả về ID để frontend fetch thông tin chi tiết
        'role': 'customer' # Backend chưa có logic role, mặc định là customer
    }, status=status.HTTP_200_OK)


# --- LOGOUT ---
@api_view(['POST'])
@require_session_auth
def api_logout(request):
    try:
        del request.session['user_id']
        del request.session['user_email']
    except KeyError:
        pass
    request.session.flush()
    return Response({'message': 'Đăng xuất thành công.'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_customer(request, customer_id):
    """
    API endpoint để lấy thông tin khách hàng bằng mongo_id.
    """
    try:
        # Sửa: Truy vấn bằng 'id' (MongoEngine tự động chuyển str thành ObjectId)
        # Sử dụng .get() để khớp chính xác (ném DoesNotExist nếu không tìm thấy)
        customer = Customer.objects.get(id=customer_id)
        
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except DoesNotExist:
        # Mô phỏng get_object_or_404: Trả về 404 nếu không tìm thấy
        return Response({'error': 'Không tìm thấy khách hàng.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Xử lý các lỗi khác (ví dụ: định dạng ObjectId không hợp lệ)
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PATCH'])
def update_customer(request, customer_id):
    """
    API endpoint để cập nhật thông tin khách hàng.
    """
    try:
        customer = Customer.objects.get(id=customer_id)
        
        # Truyền instance vào serializer
        serializer = CustomerSerializer(instance=customer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save() # Lưu các thay đổi vào database
            
            # Xây dựng phản hồi đúng như frontend mong đợi
            response_data = {
                "message": "Profile updated successfully",
                "customer": serializer.data # serializer.data chứa object đã được cập nhật
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
    except DoesNotExist:
        return Response(
            {"error": "Không tìm thấy khách hàng với ID này."},
            status=status.HTTP_404_NOT_FOUND
        )
    except ValidationError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )