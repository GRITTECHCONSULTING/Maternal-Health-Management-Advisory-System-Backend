"""
Django settings for mhmas project.
"""
 
from pathlib import Path
from decouple import config
import os
 
# ------------------------------------------------------------
# Basic Configuration
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
 
SECRET_KEY = 'django-insecure-+ylq-op1%zt!v$lh@)+bi-tc-87k)hotjzwz33$q7b40lb3e%*'
 
DEBUG = config('DEBUG', default=True, cast=bool)
 
ALLOWED_HOSTS = [
    config('LAMBDA_FUNCTION_URL', default='*'),
    'localhost',
    '127.0.0.1',
    'http://127.0.0.1:8000/',
    'https://master.dvco5e2ww6po8.amplifyapp.com/',
]
 
# ------------------------------------------------------------
# Installed Apps
# ------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'api',
    'corsheaders',
    'rest_framework_simplejwt',
    # 'storages',  # Commented out until S3 is configured
]
 
# ------------------------------------------------------------
# Middleware
# ------------------------------------------------------------
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
 
# Configure CORS - Allow all for testing
CORS_ALLOW_ALL_ORIGINS = True  # For testing only
CORS_ALLOW_CREDENTIALS = True
 
# ------------------------------------------------------------
# Lambda Function URL Configuration - FIX REDIRECT LOOP
# ------------------------------------------------------------
APPEND_SLASH = False  # Disable automatic trailing slash redirects
SECURE_SSL_REDIRECT = False  # Don't force HTTPS redirects (Lambda handles this)
USE_X_FORWARDED_HOST = True  # Trust Lambda's proxy headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # Trust HTTPS from Lambda
 
# ------------------------------------------------------------
# URL and WSGI
# ------------------------------------------------------------
ROOT_URLCONF = 'mhmas.urls'
 
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
 
WSGI_APPLICATION = 'mhmas.wsgi.application'
 
# ------------------------------------------------------------
# Database Configuration - FIXED FOR LAMBDA
# ------------------------------------------------------------
# Lambda filesystem is read-only except /tmp
# Detect if we're in AWS Lambda
IS_LAMBDA = os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None
 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': '/tmp/db.sqlite3' if IS_LAMBDA else BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'grittech',  # the name you created in DataGrip
        'USER': 'postgres',      # your postgres username
        'PASSWORD': 'amarachi',  # your postgres password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

 
# NOTE: /tmp database will reset between Lambda cold starts
# For production, use PostgreSQL with RDS
 
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
 
# ------------------------------------------------------------
# Password Validation
# ------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
 
# ------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
 
# ------------------------------------------------------------
# Static & Media Files - FIXED FOR LAMBDA
# ------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/static/'  # MUST use /tmp in Lambda!
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
 
# Media files - disabled until S3 is configured
MEDIA_URL = '/media/'
MEDIA_ROOT = '/tmp/media/'  # MUST use /tmp in Lambda!
 
# S3 Configuration (uncomment when ready to use S3)
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = config('AWS_REGION', default='us-east-1')
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
 
# ------------------------------------------------------------
# Django REST Framework
# ------------------------------------------------------------
# REST_FRAMEWORK = {
#     'DEFAULT_RENDERER_CLASSES': [
#         'rest_framework.renderers.JSONRenderer',
#     ]
# }

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
#     'ROTATE_REFRESH_TOKENS': False,
#     'BLACKLIST_AFTER_ROTATION': False,
#     'ALGORITHM': 'HS256',
#     # 'SIGNING_KEY': SECRET_KEY,  # default uses Django SECRET_KEY
#     # other options you can tune...
# }

# ------------------------------------------------------------
# drf-spectacular Settings (Swagger/OpenAPI)
# ------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'MHMAS API',
    'DESCRIPTION': 'Mobile Health Monitoring and Alert System API Documentation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
}

 
# ------------------------------------------------------------
# Logging
# ------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
    },
    'root': {
        'handlers': ['console'],
        'level': config('LOG_LEVEL', default='INFO'),
    },
}
 
# ------------------------------------------------------------
# Default Primary Key
# ------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = "api.User"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "christopheramah1@gmail.com"
EMAIL_HOST_PASSWORD = "Babcockuniversity123"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


APPEND_SLASH = True
