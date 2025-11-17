#!/usr/bin/env python
"""
Script để tạo admin user mới.
Sử dụng: python create_admin.py
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models.admin import Admin


def create_admin():
    print("=== TẠO ADMIN USER ===\n")
    
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    full_name = input("Full Name (optional): ").strip()
    
    if not username or not email or not password:
        print("❌ Username, email và password là bắt buộc!")
        return
    
    if Admin.objects(email=email).first():
        print(f"❌ Email {email} đã được sử dụng!")
        return
    
    if Admin.objects(username=username).first():
        print(f"❌ Username {username} đã được sử dụng!")
        return
    
    try:
        admin = Admin(
            username=username,
            email=email,
            full_name=full_name,
            role='admin',
            is_active=True
        )
        admin.set_password(password)
        admin.save()
        
        print(f"\n✅ Admin user '{username}' đã được tạo thành công!")
        print(f"   Email: {email}")
        print(f"   Role: {admin.role}")
        
    except Exception as e:
        print(f"❌ Lỗi khi tạo admin: {str(e)}")


if __name__ == '__main__':
    create_admin()
