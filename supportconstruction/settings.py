"""
Django settings for supportconstruction project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6bje*tq*g8supl0s*%(ik2l4#o0c^$mbmdymg@$x_nsjq@!bm)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['M0hamady.pythonanywhere.com','127.0.0.1','www.support-constructions.com','www.backend.support-constructions.com' , 'http://localhost']
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'markting',
    'client',
    'website',
    'teamview',
    'designer',
    'technical',
    'corsheaders',
    'project',
    # 'storages',
    'manager',
    'widget_tweaks',
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

ROOT_URLCONF = 'supportconstruction.urls'

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

WSGI_APPLICATION = 'supportconstruction.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
CORS_ORIGIN_ALLOW_ALL = True

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL ='login'
AUTH_USER_MODEL = 'manager.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MESSENGER_PAGE_ACCESS_TOKEN = 'EAAE96qTZA4hMBO9VSetO3bsNxjBWlrfRjVtYsZBa9QAkWZAfsdIh7xCuZCV3VrzFTxs2bARgsZAd9NxqDlUvgoq0xVz2oX808vK9QQOEU2pOD1WvYpyujapTp4M4X2ZA3vQtrx7DKLzhBA7BDYQEwlZBFceaE8PizzcOF9m9PIA8wdVg36asONCpZCCJEqRtf8P95krZApjkS'
MESSENGER_VERIFY_TOKEN = 'EAAE96qTZA4hMBO9VSetO3bsNxjBWlrfRjVtYsZBa9QAkWZAfsdIh7xCuZCV3VrzFTxs2bARgsZAd9NxqDlUvgoq0xVz2oX808vK9QQOEU2pOD1WvYpyujapTp4M4X2ZA3vQtrx7DKLzhBA7BDYQEwlZBFceaE8PizzcOF9m9PIA8wdVg36asONCpZCCJEqRtf8P95krZApjkS'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# Configure Amazon S3 settings
AWS_ACCESS_KEY_ID = 'AKIASCYPPLGYMYOM4HM7'
AWS_SECRET_ACCESS_KEY = 'N99vYeyp1Y9o+q5ONTLppOmDKmfnRGszuHGobFux'
AWS_STORAGE_BUCKET_NAME = 'supportconnstruction'
AWS_S3_REGION_NAME = 'us-east-1'  # e.g., 'us-west-1'
# default static files settings for PythonAnywhere.
# see https://help.pythonanywhere.com/pages/DjangoStaticFiles for more info
MEDIA_ROOT = '/home/M0hamady/supportconstruction/media'
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static/')]
