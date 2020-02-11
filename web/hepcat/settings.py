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

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.environ.get('DEBUG', False))
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split()
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',  # CUSTOM added for django-newsletter
    'django.contrib.messages',
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
        # 'DIRS': [],
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


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'HOST': os.environ.get('DB_HOST'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS', 'postgres'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'TEST': {
            'NAME': 'test_db'
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Media files (as uploaded by users who have permission)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CUSTOM Additional Settings for this Project

# Django Registration and email
AUTH_USER_MODEL = 'users.UserHC'
LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = 'home'
ACCOUNT_ACTIVATION_DAYS = 1
DOMAIN = os.environ.get('DOMAIN', 'localhost')
ADMIN_ID = os.environ.get('ADMIN_ID', 'webmaster')
admin_ids = ADMIN_ID.split((','))
ADMINS = [(ea, f"{ea}@{DOMAIN}") for ea in admin_ids]
manager_ids = os.environ.get('MANAGER_ID', '').split(',')
MANAGERS = [(ea, f"{ea}@{DOMAIN}") for ea in manager_ids if ea]
MANAGERS.extend(ADMINS)  # TODO: Create a flag in ENV settings to decide if all ADMINS are also MANAGERS
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', ADMINS[0][1])  # TODO: ? Different process needed?
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL')

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
PAYMENT_HOST = 'localhost'
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
