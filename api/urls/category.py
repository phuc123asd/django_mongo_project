from django.urls import path
from api.views.category import category_list

urlpatterns = [
    path('', category_list, name='category_list'),
]
