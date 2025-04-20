from pathlib import Path
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-@4#=*avo)0+f$*8jd9(eg6a!yi^mayv7lbrvqj3#$v#f5vwc%v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'drf_yasg',
    'drf_spectacular',
    'rest_framework',
    'rest_framework_simplejwt',  # Adicionado para o JWT
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  
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

WSGI_APPLICATION = 'api.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # Tempo de vida do token de acesso (5 minutos)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # Tempo de vida do token de refresh (1 dia)
    'ROTATE_REFRESH_TOKENS': True,                   # Rotaciona o refresh token ao utilizá-lo
    'BLACKLIST_AFTER_ROTATION': True,                # Revoga o token de acesso quando o refresh é feito
    'ALGORITHM': 'HS256',                            # Algoritmo para assinar o token JWT
    'SIGNING_KEY': 'your-secret-key',                # Chave secreta para assinatura dos tokens (substitua pela sua chave secreta)
    'VERIFYING_KEY': None,                           # Chave pública para verificar o token (opcional)
    'AUTH_HEADER_TYPES': ('Bearer',),                # Tipo de header para enviar o token (padrão é 'Bearer')
    'USER_ID_FIELD': 'id',                           # Campo do usuário que será utilizado para armazenar o id no token
    'USER_ID_CLAIM': 'user_id',                      # Nome do campo onde o ID do usuário será armazenado no token
}

# DRF Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT Authentication
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Permissão para requerer autenticação
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',  # Permitir parsing de JSON
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',  # Respostas no formato JSON
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # Usando o drf_spectacular para documentação
}

# Spectacular Settings (para documentação Swagger)
SPECTACULAR_SETTINGS = {
    "TITLE": "API de Vendas e Produtos",
    "DESCRIPTION": "Uma API para gerenciar vendas e produtos com verificação de estoque.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,  # Não incluir o schema na UI do Swagger
}

# Static files (CSS, JavaScript, images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
