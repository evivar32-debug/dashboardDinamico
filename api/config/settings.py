import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURIDAD: En producción, esto DEBE venir del .env
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-default-change-me')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Manejo robusto de HOSTS
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Librerías Externas
    'corsheaders',  
    'rest_framework',
    'rest_framework_simplejwt', # Añadido explícitamente
    
    # Apps Propias
    'sensores', 
    'usuarios',
]

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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Recomendado para tu index.html
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database - Configuración de PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'db'), # 'db' es el nombre del servicio en Docker
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Localización (Ajustado para Chile)
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True # Crucial para que los logs de telemetría coincidan con la hora real

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Autenticación Personalizada
AUTH_USER_MODEL = 'usuarios.Usuario'

# Configuración de CORS
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:8000').split(',')
# Durante desarrollo en CachyOS, puedes descomentar la siguiente si tienes problemas:
# CORS_ALLOW_ALL_ORIGINS = True 

# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', # Útil para el Browsable API
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        # IMPORTANTE: Cambiado a AllowAny para permitir la ingesta de datos IoT 
        # sin tokens complejos inicialmente. Luego puedes usar IsAuthenticatedOrReadOnly.
        'rest_framework.permissions.AllowAny', 
    ]
}