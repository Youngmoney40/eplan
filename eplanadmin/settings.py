import os
from pathlib import Path
from datetime import timedelta
import secrets
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from a .env file if available

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', secrets.token_urlsafe(50))

# SECURITY WARNING: don't run with debug turned on in production!
#////////////////////////////////////////////////////////////////////////////////////////////////////////
#DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
DEBUG = False


ALLOWED_HOSTS = ['plan.essential.ng', 'www.plan.essential.ng', '127.0.0.1', 'localhost']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'channels',
    'api',
]

# Redis Channels layer configuration 
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

ASGI_APPLICATION = 'eplanadmin.asgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=6000),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eplanadmin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eplanadmin.wsgi.application'

# Database 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://plan.essential.ng",
]

CSRF_TRUSTED_ORIGINS = [
    "https://plan.essential.ng",
]

#HTTPS settings
SECURE_HSTS_SECONDS = 31536000  # value for HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True  # all connections are redirected to HTTPS

# Session and CSRF settings
SESSION_COOKIE_SECURE = True  # secure cookies for sessions
CSRF_COOKIE_SECURE = True      # secure cookies for CSRF

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin dashboard theme UI settings
JAZZMIN_SETTINGS = {
    "site_title": "e-plan",
    "site_header": "E-plan Admin",
    "welcome_sign": "Welcome to E-Plan",
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
    ],
    "user_avatar": None,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
}

# WebSocket settings
CSP_CONNECT_SRC = ("'self'", "ws://127.0.0.1:8000", "ws://localhost:8000", "wss://plan.essential.ng")

