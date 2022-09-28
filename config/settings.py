"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import datetime
import os
from pathlib import Path

from decouple import config

from log.logging_formatters import CustomJsonFormatter


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps
    'corsheaders',
    'django_filters',
    'django_celery_beat',
    'drf_yasg',

    'phonenumber_field',
    'rest_framework',
    'rest_framework_simplejwt',

    'account',
    'adds',
    'info',
    'chat',
    'social_auth',
    'admin_rights',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'adds.middleware.FirstMiddleware',
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

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': config('DB_NAME'),
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'account.backends.JWTAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'logging_formatter.exception_handler.handle_exception'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=600),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=3),
}

AUTH_USER_MODEL = 'account.User'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')


JWT_SECRET_KEY = config('JWT_SECRET_KEY')

CORS_ORIGIN_ALLOW_ALL = True

REDIS_HOST = "0.0.0.0"
REDIS_PORT = "6379"
CELERY_BROKER_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_RESULT_BACKEND = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#
#     # 'formatters': {
#     #     'main_formatter': {
#     #     '()': CustomJsonFormatter
#     #     },
#     # },
#     'formatters': {
#         'simple': {
#             'format': '%(asctime)s [%(module)s | %(levelname)s] %(message)s',
#         },
#         'verbose': {
#             'format': '%(asctime)s [%(module)s | %(levelname)s] %(message)s @ %(pathname)s : %(lineno)d : %(funcName)s',
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#         'debug': {
#             'class': 'logging.FileHandler',
#             'filename': 'log/django.log',
#             'formatter': 'simple',
#             'level': 'DEBUG'
#         },
#         'error': {
#             'class': 'logging.FileHandler',
#             'filename': 'log/django.log',
#             'formatter': 'verbose',
#             'level': 'ERROR'
#         },
#         'info': {
#             'class': 'logging.FileHandler',
#             'filename': 'log/django.log',
#             'formatter': 'simple',
#             'level': 'INFO'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ["error", "info", "error"],
#             "level": 1,
#         },
#     },
# }

LOGGING = {
   'version': 1,
   'disable_existing_loggers': True,
   'filters': {
       'filter_info_level': {
           '()': 'logging_formatter.log_middleware.FilterLevels',
           'filter_levels' : [
               "INFO"
           ]
       },
       'filter_error_level': {
           '()': 'logging_formatter.log_middleware.FilterLevels',
           'filter_levels' : [
               "ERROR"
           ]
       },
       'filter_warning_level': {
           '()': 'logging_formatter.log_middleware.FilterLevels',
           'filter_levels' : [
               "WARNING"
           ]
       }
   },
   'formatters': {
       'info-formatter': {
           'format': '%(asctime)s [%(module)s | %(levelname)s] %(message)s',
       },
       'error-formatter': {
           'format': '%(asctime)s [%(module)s | %(levelname)s] %(message)s @ %(pathname)s : %(lineno)d : %(funcName)s',
           'datefmt': '%Y-%m-%d %H:%M'
       },
       'short': {
           'format': '%(levelname)s : %(message)s'
       }
   },
   'handlers': {
       'customHandler_1': {
           'formatter': 'info-formatter',
           'class': 'logging_formatter.log_middleware.DatabaseLoggingHandler',
           'database': 'logging_formatter',
           'collection': 'logs',
           'filters': ['filter_info_level'],
       },
       'customHandler_2': {
           'formatter': 'error-formatter',
           'class': 'logging_formatter.log_middleware.DatabaseLoggingHandler',
           'database': 'logging_formatter',
           'collection': 'logs',
           'filters': ['filter_error_level'],
       },
       'customHandler_3': {
           'formatter': 'short',
           'class': 'logging.StreamHandler',
           'filters': ['filter_warning_level'],
       },
   },
   'loggers': {
       'customLogger': {
           'handlers': [
               'customHandler_1',
               'customHandler_2',
               'customHandler_3'
           ],
           'level': 'DEBUG',
       },
   },
}