from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from typing import Any
from bson import ObjectId
from api.models.contact import Contact
from api.serializers.contact import ContactSerializer, ContactListSerializer
from django.core.mail import send_mail
from django.conf import settings
from mongoengine.errors import DoesNotExist

def _objects(model: Any) -> Any:
    return model.objects

@api_view(['POST'])
def create_contact(request):
    """
    Tạo tin nhắn liên hệ mới
    POST: /api/contact/
    """
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Tin nhắn của bạn đã được gửi thành công!',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'message': 'Có lỗi xảy ra',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def contact_list(request):
    """
    Lấy danh sách tất cả contact (cho admin)
    GET: /api/contact/
    """
    contacts = _objects(Contact).all().order_by('-created_at')
    serializer = ContactListSerializer(contacts, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'count': len(contacts)
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def contact_detail(request, contact_id):
    """
    Xem chi tiết 1 contact
    GET: /api/contact/<contact_id>/
    """
    try:
        contact = _objects(Contact).get(id=ObjectId(contact_id))
    except DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy tin nhắn'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Mark as read
    if not contact.is_read:
        contact.is_read = True
        contact.save()
    
    serializer = ContactSerializer(contact)
    return Response({
        'success': True,
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
def update_contact(request, contact_id):
    """
    Cập nhật tin nhắn (thêm reply từ admin)
    PUT/PATCH: /api/contact/<contact_id>/
    """
    try:
        contact = _objects(Contact).get(id=ObjectId(contact_id))
    except DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy tin nhắn'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Lấy flag send_email từ request
    send_email = request.data.get('send_email', False)
    
    serializer = ContactSerializer(contact, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        
        # Gửi email nếu có reply và send_email = True
        if send_email and 'reply' in request.data and request.data['reply']:
            try:
                send_reply_email(contact.email, contact.name, request.data['reply'], contact.subject)
            except Exception as e:
                print(f"Lỗi khi gửi email: {str(e)}")
                # Vẫn trả về success nếu cập nhật thành công, email là phụ
        
        return Response({
            'success': True,
            'message': 'Cập nhật thành công',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    return Response({
        'success': False,
        'message': 'Có lỗi xảy ra',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


def send_reply_email(customer_email, customer_name, reply_message, subject):
    """
    Hàm gửi email phản hồi cho khách hàng
    """
    email_subject = f'Re: {subject}'
    email_body = f"""
Xin chào {customer_name},

Cảm ơn bạn đã liên hệ với chúng tôi. Dưới đây là phản hồi của chúng tôi:

---
{reply_message}
---

Nếu bạn có thêm câu hỏi, vui lòng liên hệ với chúng tôi lại.

Trân trọng,
TechHub Support Team
support@techhub.com
    """
    
    send_mail(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [customer_email],
        fail_silently=False,
    )


@api_view(['DELETE'])
def delete_contact(request, contact_id):
    """
    Xóa tin nhắn
    DELETE: /api/contact/<contact_id>/
    """
    try:
        contact = _objects(Contact).get(id=ObjectId(contact_id))
        contact.delete()
        return Response({
            'success': True,
            'message': 'Xóa thành công'
        }, status=status.HTTP_200_OK)
    except DoesNotExist:
        return Response({
            'success': False,
            'message': 'Không tìm thấy tin nhắn'
        }, status=status.HTTP_404_NOT_FOUND)
