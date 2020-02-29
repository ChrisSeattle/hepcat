"""
Django settings for hepcat project.
Generated by 'django-admin startproject' using Django 2.1.3.
For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from distutils.util import strtobool

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL = True if BASE_DIR == os.environ.get('LOCAL_BASE_DIR') else False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', None)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.environ.get('DEBUG', 'False'))
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS' if LOCAL else 'LIVE_ALLOWED_HOSTS', '').split()
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',  # CUSTOM added for django-newsletter
    'django.contrib.messages',
    'storages',  # CUSTOM django-storages for using AWS S3 for static files
    'django.contrib.staticfiles',
    # 'rest_framework',
    # 'rest_framework.authtoken',
    'django_registration',  # CUSTOM
    'payments',  # CUSTOM for payment processing
    # Imperavi (or tinymce) rich text editor is optional
    # 'imperavi',
    # 'sorl.thumbnail',  # CUSTOM required for newsletter
    # 'newsletter',  # CUSTOM for email newsletters.
    'hepcat',  # CUSTOM: Project name
    'classwork',  # CUSTOM: App name
    'users',  # CUSTOM: App name
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
ROOT_URLCONF = 'hepcat.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # CUSTOM: Added when adding users model app
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
WSGI_APPLICATION = 'hepcat.wsgi.application'

# Database https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# if 'RDS_HOSTNAME' in os.environ:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': os.environ['RDS_DB_NAME'],
#             'USER': os.environ['RDS_USERNAME'],
#             'PASSWORD': os.environ['RDS_PASSWORD'],
#             'HOST': os.environ['RDS_HOSTNAME'],
#             'PORT': os.environ['RDS_PORT'],
#         }
#     }
# else:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('LOCAL_DB_HOST' if LOCAL else 'LIVE_DB_HOST', os.environ.get('DB_HOST', '')),
        'PORT': os.environ.get('LOCAL_DB_PORT' if LOCAL else 'LIVE_DB_PORT', os.environ.get('DB_PORT', '5432')),
        'NAME': os.environ.get('LOCAL_DB_NAME' if LOCAL else 'LIVE_DB_NAME', os.environ.get('DB_NAME', 'postgres')),
        'USER': os.environ.get('LOCAL_DB_USER' if LOCAL else 'LIVE_DB_USER', os.environ.get('DB_USER', 'postgres')),
        'PASSWORD': os.environ.get('LOCAL_DB_PASS' if LOCAL else 'LIVE_DB_PASS', os.environ.get('DB_PASS', '')),
        # 'TEST': {
        #     'NAME': 'test_db'
        # }
    }
}
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'en-us')
TIME_ZONE = os.environ.get('TIME_ZONE', 'America/Los_Angeles')
USE_I18N = True
USE_L10N = True
USE_TZ = True
# Static files (CSS, JavaScript, Images) https://docs.djangoproject.com/en/2.1/howto/static-files/
USE_S3 = strtobool(os.environ.get('USE_S3', 'False'))
if USE_S3:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
    AWS_DEFAULT_ACL = None
    # AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3-website-{AWS_S3_REGION_NAME}.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_LOCATION = 'www'
    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'web.storage_backends.StaticStorage'
    MEDIAFILES_LOCATION = 'media'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # TODO: Seems to still keep them on EC2 not S3
    # DEFAULT_FILE_STORAGE = 'web.storage_backends.PublicMediaStorage'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    # STATIC_ROOT = os.path.join(BASE_DIR, '..', 'www', 'static')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    # MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'www', 'media')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# CUSTOM Additional Settings for this Project

# Django Registration and email
AUTH_USER_MODEL = 'users.UserHC'
LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = 'home'
ACCOUNT_ACTIVATION_DAYS = 1
EMAIL_DOMAIN = os.environ.get('EMAIL_DOMAIN', 'localhost')
EMAIL_ADMIN_ID = os.environ.get('EMAIL_ADMIN_ID', 'webmaster')
admin_ids = EMAIL_ADMIN_ID.split((','))
ADMINS = [(ea, f"{ea}@{EMAIL_DOMAIN}") for ea in admin_ids]
manager_ids = os.environ.get('EMAIL_MANAGER_ID', '').split(',')
MANAGERS = [(ea, f"{ea}@{EMAIL_DOMAIN}") for ea in manager_ids if ea]
EMAIL_ADMIN_ARE_MANAGERS = strtobool(os.environ.get('EMAIL_ADMIN_ARE_MANAGERS', 'False'))
if EMAIL_ADMIN_ARE_MANAGERS:
    MANAGERS.extend(ADMINS)
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_DEFAULT_FROM', ADMINS[0][1])
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '25'))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = strtobool(os.environ.get('EMAIL_USE_TLS', 'False'))
EMAIL_USE_SSL = strtobool(os.environ.get('EMAIL_USE_SSL', 'False'))
EMAIL_SUBJECT_PREFIX = '[' + os.environ.get('EMAIL_ADMIN_PREFIX', 'Django') + '] '
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# else:
#     Handle all of the configs for a real email SMTPBackend

# Django Newsletter
# NEWSLETTER_CONFIRM_EMAIL = False
# Using django-tinymce
# NEWSLETTER_RICHTEXT_WIDGET = "tinymce.widgets.TinyMCE"
# Amount of seconds to wait between each email. Here 100ms is used.
NEWSLETTER_EMAIL_DELAY = 0.1
# Amount of seconds to wait between each batch. Here one minute is used.
NEWSLETTER_BATCH_DELAY = 60
# Number of emails in one batch
NEWSLETTER_BATCH_SIZE = 100

# CUSTOM Settings for Payment Processing
STRIPE_KEY = os.environ.get('STRIPE_KEY', None)
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', None)
PAYPAL_EMAIL = os.environ.get('PAYPAL_EMAIL', None)
PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID', None)
PAYPAL_SECRET = os.environ.get('PAYPAL_SECRET', None)
PAYPAL_URL = os.environ.get('PAYPAL_URL', 'https://api.sandbox.paypal.com')  # https://api.paypal.com for production
PAYMENT_HOST = os.environ.get('PAYMENT_HOST', 'localhost')
PAYMENT_USES_SSL = False
PAYMENT_MODEL = 'classwork.Payment'
PAYMENT_VARIANTS = {
    'paypal': ('payments.paypal.PaypalProvider', {
        'client_id': PAYPAL_CLIENT_ID,
        'secret': PAYPAL_SECRET,
        'endpoint': PAYPAL_URL,
        'capture': False}),
    'stripe': ('payments.stripe.StripeProvider', {
        'secret_key': STRIPE_KEY,
        'public_key': STRIPE_PUBLIC_KEY
        }),
    'default': ('payments.dummy.DummyProvider', {})
    }

# CUSTOM Global variables
DEFAULT_CLASS_PRICE = os.environ.get('DEFAULT_CLASS_PRICE', None)
DEFAULT_PRE_DISCOUNT = os.environ.get('DEFAULT_PRE_DISCOUNT', None)
MULTI_DISCOUNT = os.environ.get('MULTI_DISCOUNT', None)
