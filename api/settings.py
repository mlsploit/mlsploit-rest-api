"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 1.11.18.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCRATCH_DIR = os.path.join(BASE_DIR, ".scratch")
os.makedirs(SCRATCH_DIR, exist_ok=True)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("MLSPLOIT_API_SECRET_KEY")
assert (
    SECRET_KEY and len(SECRET_KEY) >= 25
), """
    MLSPLOIT_API_SECRET_KEY environment variable not found or too short (min length: 25).

    If running via entrypoint.sh, then set it in the .env file, otherwise run the following command:
    $ export MLSPLOIT_API_SECRET_KEY='e(@0oj#c9u=qva@g&)*(rx7m9_vf!!h!#b(sg(%nr2rk+p)+v1'

    SECURITY WARNING: This is an example secret key, keep the secret key used in production a secret.
    """


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("MLSPLOIT_API_DEBUG_MODE") == "true"

ALLOWED_HOSTS = os.getenv("MLSPLOIT_API_ALLOWED_HOSTS")
if ALLOWED_HOSTS is None:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ALLOWED_HOSTS.split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_auth.registration",
    "corsheaders",
    "django_filters",
    "coreapi",
    "users",
    "modules",
    "files",
    "pipelines",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True
USE_X_FORWARDED_HOST = True
ROOT_URLCONF = "api.urls"

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

WSGI_APPLICATION = "api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DB_PATH = os.path.join(SCRATCH_DIR, "data", "db.sqlite3")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": DB_PATH}}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/api/static/"


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

REST_AUTH_SERIALIZERS = {
    "TOKEN_SERIALIZER": "users.serializers.TokenSerializer",
    "USER_DETAILS_SERIALIZER": "users.serializers.UserSerializer",
}

ACCOUNT_AUTHENTICATION_METHOD = "username"
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False

MEDIA_URL = "/media/"
MEDIA_DIR = os.path.join(SCRATCH_DIR, "media")
os.makedirs(MEDIA_DIR, exist_ok=True)
