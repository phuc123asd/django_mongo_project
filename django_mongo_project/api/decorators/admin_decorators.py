from functools import wraps
from django.http import JsonResponse
from rest_framework import status


def require_admin_auth(view_func):
    """
    Decorator để yêu cầu admin phải đăng nhập.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'admin_id' not in request.session:
            return JsonResponse(
                {'error': 'Yêu cầu đăng nhập với quyền admin.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return view_func(request, *args, **kwargs)
    return wrapper


def require_super_admin(view_func):
    """
    Decorator để yêu cầu super admin role.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        admin_role = request.session.get('admin_role')
        
        if not admin_role or admin_role != 'super_admin':
            return JsonResponse(
                {'error': 'Yêu cầu quyền super admin.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request, *args, **kwargs)
    return wrapper
