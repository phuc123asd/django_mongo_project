from django.urls import path, include

urlpatterns = [
    path('products/', include('api.urls.product')),
    path('categories/', include('api.urls.category')),
    path('customer/', include('api.urls.customer')),
    path('admin/', include('api.urls.admin_auth')),
    path('admin/customers/', include('api.urls.customer_admin')),
    path('admin/reviews/', include('api.urls.review_admin')),
    path('admin/dashboard/', include('api.urls.dashboard')),
    path('order/', include('api.urls.order')),
    path('review/', include('api.urls.review')),
    path('chatbot/', include('api.urls.chatbot')),
    path('upload-image/', include('api.urls.upload_image')),
]
