# TechHub - E-commerce Platform

## Overview
TechHub là một nền tảng thương mại điện tử full-stack với tính năng AI chatbot và tự động phản hồi đánh giá.

## Cấu trúc Dự án

### Backend (Django + MongoDB)
- **Đường dẫn**: `django_mongo_project/`
- **Framework**: Django 4.2.8 + MongoDB (MongoEngine)
- **Database**: 
  - SQLite: Cho Django admin và auth
  - MongoDB Atlas: Cho dữ liệu ứng dụng (products, orders, reviews, customers)
  - DataStax Astra DB: Cho vector search (chatbot)

### Frontend (React + Vite)
- **Đường dẫn**: `frontend/`
- **Framework**: React 18 + TypeScript + Vite
- **UI**: TailwindCSS
- **Chức năng**: Website thương mại điện tử cho khách hàng

### Admin Panel
- **Đường dẫn**: `admin/`
- **Framework**: React 18 + TypeScript + Vite
- **Chức năng**: Quản lý sản phẩm, đơn hàng, đánh giá

## Tính năng Chính

### 1. Quản lý Sản phẩm
- Xem danh sách sản phẩm
- Chi tiết sản phẩm
- Phân loại theo danh mục

### 2. Quản lý Người dùng
- Đăng ký / Đăng nhập
- Quản lý hồ sơ
- Lịch sử đơn hàng

### 3. Giỏ hàng & Đặt hàng
- Thêm/xóa sản phẩm khỏi giỏ hàng
- Thanh toán
- Theo dõi đơn hàng

### 4. Đánh giá Sản phẩm với AI Auto-Response
- Khách hàng có thể đánh giá sản phẩm (1-5 sao)
- **TỰ ĐỘNG TẠO PHẢN HỒI** bằng OpenAI:
  - **< 3 sao**: Phản hồi thể hiện sự quan tâm và đề nghị hỗ trợ
  - **>= 3 sao**: Phản hồi cảm ơn khách hàng
- Hệ thống tự động lưu phản hồi vào database

### 5. AI Chatbot
- Tư vấn sản phẩm thông minh
- Vector search với Astra DB
- Trả lời tự nhiên với OpenAI GPT-4

## Cấu hình Môi trường

### Biến môi trường bắt buộc (Django Backend)

Các biến này được đặt trong `django_mongo_project/.env`:

```bash
# Django Security
SECRET_KEY=<your-django-secret-key>
DEBUG=True  # Set False in production

# OpenAI (BẮT BUỘC cho auto-response reviews và chatbot)
OPENAI_API_KEY=<your-openai-api-key>

# Astra DB (Tùy chọn - cho vector search trong chatbot)
ASTRA_DB_APPLICATION_TOKEN=<your-astra-token>
ASTRA_API_ENDPOINT=<your-astra-endpoint>
```

### Frontend Environment
File `frontend/.env`:
```bash
VITE_API_URL=https://<your-replit-domain>:8000/api
```

## Cách chạy Dự án

### Development Mode (Replit)
Workflow tự động khởi động cả backend và frontend:
- **Backend**: Django dev server trên port 8000
- **Frontend**: Vite dev server trên port 5000
- Chỉ cần nhấn Run!

### Production Deployment
Khi publish trên Replit:
- Frontend được build thành static files
- Backend chạy với Gunicorn
- Cả hai được serve cùng lúc

## API Endpoints

### Products
- `GET /api/products/` - Danh sách sản phẩm
- `GET /api/products/{id}/` - Chi tiết sản phẩm

### Categories
- `GET /api/categories/` - Danh sách danh mục

### Customer
- `POST /api/customer/register/` - Đăng ký
- `POST /api/customer/login/` - Đăng nhập
- `POST /api/customer/logout/` - Đăng xuất
- `GET /api/customer/get_customer/{id}/` - Thông tin khách hàng
- `PATCH /api/customer/up_date/{id}/` - Cập nhật thông tin

### Orders
- `POST /api/order/create/` - Tạo đơn hàng
- `GET /api/order/customer/{customer_id}/` - Đơn hàng của khách
- `GET /api/order/{order_id}/` - Chi tiết đơn hàng

### Reviews (WITH AUTO-RESPONSE)
- `GET /api/review/get_by_id/{product_id}/` - Đánh giá của sản phẩm
- `POST /api/review/add/` - Thêm đánh giá **→ TỰ ĐỘNG TẠO PHẢN HỒI AI**

### Chatbot
- `POST /api/chatbot/` - Chat với AI

### Upload
- `POST /api/upload-image/` - Upload ảnh

## Công nghệ Sử dụng

### Backend
- Django 4.2.8
- Django REST Framework
- MongoEngine (MongoDB ODM)
- OpenAI API
- Astra DB (DataStax)
- Gunicorn
- Cloudinary (Image storage)

### Frontend
- React 18
- TypeScript
- Vite
- TailwindCSS
- React Router DOM
- Lucide React (Icons)

## Recent Changes

### 2025-11-17: Auto-Response Feature for Reviews
- Added `admin_response` and `response_generated_at` fields to Review model
- Implemented AI-powered auto-response generation using OpenAI
- Reviews with rating < 3 stars receive supportive, help-offering responses
- Reviews with rating >= 3 stars receive grateful thank-you responses
- Fallback to default messages when OpenAI is not configured
- All review submissions now automatically include admin responses

### 2025-11-17: Initial Replit Setup
- Configured Django backend to run on port 8000
- Configured Vite frontend to run on port 5000 with Replit proxy support
- Set up environment variables for development
- Fixed Astra DB and OpenAI client initialization to handle missing credentials gracefully
- Created unified workflow to run both backend and frontend
- Configured deployment settings

## Notes

- MongoDB connection string được hardcode trong `settings.py` - nên di chuyển vào `.env` cho bảo mật
- Cloudinary credentials cũng được hardcode - nên di chuyển vào `.env`
- Review API hiện tại không yêu cầu authentication (`add_review_insecure`) - nên thêm authentication trong production
- OpenAI API key là BẮT BUỘC để auto-response và chatbot hoạt động
- Astra DB là tùy chọn - nếu không có, vector search sẽ bị vô hiệu hóa

## User Preferences

No specific user preferences recorded yet.
