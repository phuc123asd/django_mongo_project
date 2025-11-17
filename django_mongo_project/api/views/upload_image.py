from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cloudinary.uploader

@csrf_exempt
def upload_image(request):
    # --- DEBUGGING LOGS ---
    print(f"Request method: {request.method}")
    print(f"Request POST data: {request.POST}")
    print(f"Request FILES data: {request.FILES}")
    # --- END DEBUGGING LOGS ---

    if request.method == "POST" and request.FILES.get('file'):
        file = request.FILES['file']
        result = cloudinary.uploader.upload(file)
        return JsonResponse({'url': result['secure_url']})
    
    # Thay đổi thông báo lỗi để rõ ràng hơn
    error_message = 'No file uploaded' if not request.FILES.get('file') else 'Request method is not POST'
    return JsonResponse({'error': error_message}, status=400)