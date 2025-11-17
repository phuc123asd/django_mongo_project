from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models.admin import Admin
from api.serializers.admin import AdminSerializer
from datetime import datetime
from mongoengine.errors import DoesNotExist
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
def admin_register(request):
    """
    API đăng ký admin mới (chỉ dùng cho development hoặc super admin).
    """
    email = request.data.get('email')
    password = request.data.get('password')
    username = request.data.get('username')
    full_name = request.data.get('full_name', '')

    if not email or not password or not username:
        return Response(
            {'error': 'Vui lòng cung cấp email, username và mật khẩu.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if Admin.objects(email=email).first():
        return Response(
            {'error': 'Email này đã được sử dụng.'},
            status=status.HTTP_409_CONFLICT
        )
    
    if Admin.objects(username=username).first():
        return Response(
            {'error': 'Username này đã được sử dụng.'},
            status=status.HTTP_409_CONFLICT
        )

    try:
        admin = Admin(
            email=email,
            username=username,
            full_name=full_name,
            role='admin',
            is_active=True
        )
        admin.set_password(password)
        admin.save()

        return Response({
            'message': 'Admin registered successfully',
            'id': str(admin.id)
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error registering admin: {str(e)}")
        return Response(
            {'error': 'Đã có lỗi xảy ra.', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def admin_login(request):
    """
    API đăng nhập cho admin.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Vui lòng cung cấp email và mật khẩu.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        admin = Admin.objects.get(email=email)
    except DoesNotExist:
        return Response(
            {'error': 'Email hoặc mật khẩu không chính xác.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not admin.check_password(password):
        return Response(
            {'error': 'Email hoặc mật khẩu không chính xác.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not admin.is_active:
        return Response(
            {'error': 'Tài khoản admin đã bị vô hiệu hóa.'},
            status=status.HTTP_403_FORBIDDEN
        )

    admin.last_login = datetime.utcnow()
    admin.save()

    request.session['admin_id'] = str(admin.id)
    request.session['admin_email'] = admin.email
    request.session['admin_role'] = admin.role

    serializer = AdminSerializer(admin)
    
    return Response({
        'message': 'Login successful',
        'admin': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def admin_logout(request):
    """
    API đăng xuất cho admin.
    """
    try:
        del request.session['admin_id']
        del request.session['admin_email']
        del request.session['admin_role']
    except KeyError:
        pass
    
    request.session.flush()
    
    return Response(
        {'message': 'Đăng xuất thành công.'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def admin_me(request):
    """
    API lấy thông tin admin hiện tại.
    """
    admin_id = request.session.get('admin_id')
    
    if not admin_id:
        return Response(
            {'error': 'Yêu cầu đăng nhập.'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        admin = Admin.objects.get(id=admin_id)
        serializer = AdminSerializer(admin)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except DoesNotExist:
        request.session.flush()
        return Response(
            {'error': 'Admin không tồn tại.'},
            status=status.HTTP_404_NOT_FOUND
        )
