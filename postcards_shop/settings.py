from pathlib import Path

from django.conf.global_settings import STATIC_ROOT
from dotenv import load_dotenv  # Для файла конфігурації .env
import os  # Для файла конфігурації .env

load_dotenv()  # Завантаження файлу конфігурвції DB

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['ivertepny.com', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django_extensions',
    'django_celery_beat',
    'storages',

    # allAuth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    # 'social_django',
    # 'oauth2_provider',
    # 'sslserver',
    'django_recaptcha',
    'rest_framework',
    'rest_framework.authtoken',
    "graphene_django",
    "django_elasticsearch_dsl",
    'drf_yasg',

    # debug_toolbar
    "debug_toolbar",
    # my apps
    'products',
    #  ??? 'products.apps.ProductsConfig',
    'users',
    'orders',
    'telegrambot',
    'api',
    'google_sheet',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'postcards_shop.urls'

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
                'products.context_processors.baskets',
            ],
        },
    },
]

WSGI_APPLICATION = 'postcards_shop.wsgi.application'

# для debug
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
    "ivertepny.com",
]

# Redis

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/1",
    }
}

# DB Postgres

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",  # Рекомендують psycopg2#
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# MongoDB

MONGO_DB_SETTINGS = {
    'HOST': os.getenv("MONGO_DB_HOST"),
    'PORT': os.getenv("MONGO_DB_PORT"),
    'DB_NAME': os.getenv("MONGO_DB_NAME"),
    'COLLECTION': os.getenv("MONGO_DB_COLLECTION"),
    'USERNAME': os.getenv("MONGO_DB_USERNAME"),
    'PASSWORD': os.getenv("MONGO_DB_PASSWORD"),
    'URI': os.getenv("MONGO_DB_URI"),

}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'uk-uk'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# STATIC_ROOT = BASE_DIR / 'static'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Додаємо медіафайли

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Кастомізація юзера

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# робота з e-mail
DOMAIN_NAME = 'http://localhost:8000'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# if DEBUG:
#     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# else:
#     EMAIL_HOST = os.getenv('MY_EMAIL_HOST')
#     EMAIL_PORT = os.getenv('MY_EMAIL_PORT')
#     EMAIL_HOST_USER = os.getenv('MY_EMAIL_HOST_USER')
#     EMAIL_HOST_PASSWORD = os.getenv("MY_EMAIL_HOST_PASSWORD")
#     EMAIL_USE_SSL = os.getenv('MY_EMAIL_USE_SSL')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('MY_EMAIL_HOST')
EMAIL_PORT = os.getenv('MY_EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('MY_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv("MY_EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = os.getenv('MY_EMAIL_USE_SSL')

# робота з AllAuth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    # 'social_core.backends.google.GoogleOAuth2',
]

SITE_ID = 1  # GitHub+Google

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
        ],
    },
    "google": {

        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "offline",
        },
    }
}

# SOCIALACCOUNT_AUTO_SIGNUP = True
# SOCIALACCOUNT_LOGIN_ON_GET = False

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

# Celery + Redis

CELERY_BROKER_URL = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}"
CELERY_RESULT_BACKEND = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}"
# CELERY_IMPORTS = ('telegrambot.sendmessage',)
USE_DEPRECATED_PYTZ = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Stripe

STRIPE_PUBLIC_KEY = os.getenv('MY_STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('MY_STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('MY_STRIPE_WEBHOOK_SECRET')

# ReCAPTCHA

RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
# RECAPTCHA_REQUIRED_SCORE = 0.99

# REST Api

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # 'path.to.CustomAuthentication',  # Для кастомного методу аутентифікації, треба доробити!!!!!
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# GraphQL
GRAPHENE = {
    "SCHEMA": "api_graphql.schema.schema"
}

# Elasticsearch
ELASTICSEARCH_DSL = {
    'default': {
        # 'hosts': 'http://localhost:9200'
        # 'hosts': os.getenv('ELASTICSEARCH_HOST')
        'hosts': 'http://ivertepny.com:9200'
    },
}

# OpenAI

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# AWS S3
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_LOCATION = 'static'
AWS_S3_REGION_NAME = 'us-east-1'

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'


# DEFAULT_FILE_STORAGE = 'hillelDjango4.storages.MediaStorage'




