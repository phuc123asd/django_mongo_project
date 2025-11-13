from django.urls import path, include

urlpatterns = [
    path('products/', include('api.urls.product')),
    path('categories/', include('api.urls.category')),
    path('customer/', include('api.urls.customer')),
    path('order/', include('api.urls.order')),
    path('review/', include('api.urls.review')),
    path('chatbot/', include('api.urls.chatbot')),
]
