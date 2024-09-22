
from pathlib import Path
from dotenv import load_dotenv  # Для файла конфігурації .env
import os  # Для файла конфігурації .env

load_dotenv()  # Завантаження файлу конфігурвції DB

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = []

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
    # OAuth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    # debug_toolbar
    "debug_toolbar",
    # my apps
    'products',
    #  ??? 'products.apps.ProductsConfig',
    'users',
    'orders',

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
        'DIRS': []
        ,
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
    "localhost"
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

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

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
DOMAIN_NAME = 'http://127.0.0.1:8000'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_HOST = os.getenv('MY_EMAIL_HOST')
    EMAIL_PORT = os.getenv('MY_EMAIL_PORT')
    EMAIL_HOST_USER = os.getenv('MY_EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv("MY_EMAIL_HOST_PASSWORD")
    EMAIL_USE_SSL = os.getenv('MY_EMAIL_USE_SSL')

# робота з OAuth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1  # GitHub

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'user',
        ],
    }
}

# Celery

CELERY_BROKER_URL = f'redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}'
CELERY_RESULT_BACKEND = f'redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}'

# Stripe

STRIPE_PUBLIC_KEY = os.getenv('MY_STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('MY_STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('MY_STRIPE_WEBHOOK_SECRET')
