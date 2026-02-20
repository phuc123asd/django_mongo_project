from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from google.oauth2 import id_token
from google.auth.transport import requests
from api.models.customer import Customer
from decouple import config

# Client ID từ Google Console
GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID', default='')

@csrf_exempt
def google_login(request):
    """
    Xử lý đăng nhập bằng Google OAuth
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        credential = data.get('credential')
        
        if not credential:
            return JsonResponse({'error': 'Missing credential'}, status=400)
        
        # Xác thực token với Google
        try:
            idinfo = id_token.verify_oauth2_token(
                credential, 
                requests.Request(), 
                GOOGLE_CLIENT_ID
            )
            
            # Lấy thông tin user từ Google
            email = idinfo['email']
            name = idinfo.get('name', '')
            given_name = idinfo.get('given_name', '')
            family_name = idinfo.get('family_name', '')
            picture = idinfo.get('picture', '')
            
            # Kiem tra xem user da ton tai chua
            customer = Customer.objects(email=email).first()
            is_new = False
            if not customer:
                # Tao user moi neu chua ton tai
                customer = Customer(
                    email=email,
                    password='google_oauth',
                    first_name=given_name or name,
                    last_name=family_name,
                    phone='',
                    address='',
                    city='',
                    province='',
                    postal_code=''
                )
                customer.save()
                is_new = True

            # Luu thong tin vao session de dong bo voi luong login thuong
            request.session['user_id'] = str(customer.id)
            request.session['user_email'] = customer.email

            # Tra ve dinh dang giong api_login/api_register
            return JsonResponse({
                'message': 'Login successful',
                'id': str(customer.id),
                'role': 'customer'
            })
            
        except ValueError as e:
            # Token không hợp lệ
            return JsonResponse({'error': 'Invalid token', 'details': str(e)}, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
