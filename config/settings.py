"""
Django settings for config project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv  # ← əlavə edin

# --- Load .env file ---
load_dotenv()  # ← .env faylındakı environment variables-ları oxuyur

# --- Base directory ---
BASE_DIR = Path(__file__).resolve().parent.parent

CSRF_TRUSTED_ORIGINS = ['https://ecommerce-analitic-808729853617.me-west1.run.app']


# --- Security ---
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-this')
DEBUG = True
ALLOWED_HOSTS = [
    '*'
]


# serverde
CSRF_TRUSTED_ORIGINS = [
        '*'
]
##

# CSRF_TRUSTED_ORIGINS = [
#     'http://127.0.0.1:8000',       # Local server
#     'http://localhost',             # Local test
#     'https://<cloud-run-domain>'    # Cloud Run domain
# ]

# --- Applications ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'analitic',
]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# --- Database configuration (Cloud Run + Local) ---
import os

# --- DB credentials ---
DB_NAME = os.environ.get('DB_NAME', 'ecommerce_db')
DB_USER = os.environ.get('DB_USER', 'ecommerce_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '12345')
DB_PORT = os.environ.get('DB_PORT', '5432')

# Environment detection
CLOUD_SQL_CONNECTION_NAME = os.environ.get('CLOUD_SQL_CONNECTION_NAME')
LOCAL = os.environ.get('LOCAL', 'False') == 'True'  # Cloud Run üçün default False

# Host seçimi
if not LOCAL:
    # Cloud Run-da Public IP ilə qoşul
    DB_HOST = os.environ.get('DB_HOST', '34.60.148.42')
else:
    # Lokal PC
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}





# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static files ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # collectstatic üçün
STATICFILES_DIRS = [
    BASE_DIR / "static",  # lokal inkişaf üçün
]


# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
