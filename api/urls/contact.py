from django.urls import path
from api.views.contact import (
    create_contact,
    contact_list,
    contact_detail,
    update_contact,
    delete_contact
)

urlpatterns = [
    path('', create_contact, name='create_contact'),  # POST: Gửi tin nhắn
    path('list/', contact_list, name='contact_list'),  # GET: Danh sách contact
    path('<str:contact_id>/', contact_detail, name='contact_detail'),  # GET: Chi tiết contact
    path('<str:contact_id>/update/', update_contact, name='update_contact'),  # PUT/PATCH: Cập nhật
    path('<str:contact_id>/delete/', delete_contact, name='delete_contact'),  # DELETE: Xóa
]
