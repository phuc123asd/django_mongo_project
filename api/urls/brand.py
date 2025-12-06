from django.urls import path
from api.views.brand import brand_list

urlpatterns = [
    path('', brand_list, name='brand_list'),
]
