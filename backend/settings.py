"""
Django settings for backend project.
"""

from pathlib import Path
import os
from decouple import config, Csv
import mongoengine
import certifi

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure OpenSSL can locate trusted CA certificates for outbound TLS (SMTP, HTTPS).
os.environ.setdefault("SSL_CERT_FILE", certifi.where())
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())
os.environ.setdefault("CURL_CA_BUNDLE", certifi.where())

# --- BẮT ĐẦU CẤU HÌNH TỪ .ENV ---
# Đây là nơi duy nhất các biến môi trường được đọc.

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Cho phép truy cập từ các host này
ALLOWED_HOSTS = ['*']

# Đọc các API Key
OPENAI_API_KEY = config('OPENAI_API_KEY')
ASTRA_DB_APPLICATION_TOKEN = config('ASTRA_DB_APPLICATION_TOKEN')
ASTRA_API_ENDPOINT = config('ASTRA_API_ENDPOINT')


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # App của bên thứ ba
    'rest_framework',
    'corsheaders',
    'rest_framework_mongoengine',

    # App của bạn
    'mongoengine',
    'api',
    
    # Cloud lưu ảnh
    'cloudinary',
    'cloudinary_storage',
]

# settings.py
import cloudinary

cloudinary.config( 
  cloud_name = "dze6buir3", 
  api_key = "652542943279132", 
  api_secret = "gzeC-JTXYAWpP3udjSDGw06C66A"
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# Database
# Vẫn giữ lại SQLite cho các bảng mặc định của Django (admin, auth,...)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Kết nối đến MongoDB cho các model của bạn
mongoengine.connect(
    name='mydb',
    host='mongodb+srv://admin:123@cluster0.gdq3i7q.mongodb.net/?appName=Cluster0',
    tlsAllowInvalidCertificates=True  # Tạm thời bypass SSL certificate verification cho development
)


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cấu hình CORS
CORS_ALLOWED_ORIGINS = [
    "https://fontend-8jcm.onrender.com",
    "http://localhost:5173", # Cổng mặc định của Vite (React)
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
SESSION_SAVE_EVERY_REQUEST = True

# Cấu hình Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='support@techhub.com')

# Disable SSL verification for development (enable in production with proper certificates)
if DEBUG:
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
