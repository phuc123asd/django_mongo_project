# api/decorators.py
from functools import wraps
from django.http import JsonResponse
from rest_framework import status

def require_session_auth(view_func):
    """
    Decorator để kiểm tra xem user đã đăng nhập (có trong session) chưa.
    Nếu chưa, trả về lỗi 401.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Đây là logic chính của decorator
        if 'user_id' not in request.session:
            return JsonResponse(
                {'error': 'Yêu cầu đăng nhập.'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        # Nếu qua được kiểm tra, gọi hàm view gốc
        return view_func(request, *args, **kwargs)
    return _wrapped_view