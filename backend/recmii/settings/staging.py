"""
Django settings for recmii project.

Generated by 'django-admin startproject' using Django 3.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import environ
import os
from pathlib import Path

env = environ.Env()
env.read_env(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "api.apps.ApiConfig",
    "corsheaders",
    "django_ses",
    "django_celery_beat",
    "django_celery_results",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

from corsheaders.defaults import default_headers

CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST")
CORS_ALLOW_HEADERS = list(default_headers) + ["sentry-trace", "baggage"]

ROOT_URLCONF = "recmii.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "recmii.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DATABASES_NAME"),
        "USER": env("DATABASES_USER"),
        "PASSWORD": env("DATABASES_PASSWORD"),
        "HOST": env("DATABASES_HOST"),
        "PORT": "5432",
        "OPTIONS": {"client_encoding": "UTF-8"},
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Add
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "django.contrib.auth.backends.RemoteUserBackend",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        #'rest_framework.authentication.TokenAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    "JWT_PAYLOAD_GET_USERNAME_HANDLER": "api.utils.jwt_get_username_from_payload_handler",
    "JWT_DECODE_HANDLER": "api.utils.jwt_decode_token",
    "JWT_ALGORITHM": "RS256",
    "JWT_AUDIENCE": env("JWT_AUDIENCE"),
    "JWT_ISSUER": env("JWT_ISSUER"),
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
}

AUTH_USER_MODEL = "api.User"

# Django Storage
FILE_STORAGE = "s3"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")

# SES
AWS_SES_REGION_NAME = env("AWS_SES_REGION_NAME")
AWS_SES_REGION_ENDPOINT = env("AWS_SES_REGION_ENDPOINT")
EMAIL_BACKEND = "django_ses.SESBackend"
IS_EMAIL_LIMIT = True

# Celery
CELERY_BROKER_URL = env.get_value("CELERY_BROKER_URL", default="redis://redis:6379")
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"

# LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "django.db": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
        "django.contrib.auth": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}


import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


def before_send(event, hint):
    # Modify event here. If you want to ignore an event you can also just return None
    # Ignore events where path equals '/api/v1/health-check'
    if "request" in event and event["request"]["url"].endswith(
        "/api/agent/v1/health-check"
    ):
        return None
    if "request" in event and event["request"]["url"].startswith("/admin/"):
        return None
    return event


sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.1,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    before_send=before_send,
    environment="staging",
)

# OpenAI
OPENAI_API_KEY = env("OPENAI_API_KEY")
