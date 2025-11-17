from django.urls import path
from api.views.upload_image import upload_image

urlpatterns = [
    path('', upload_image),
]
