from .sensitive_settings import *

# Build paths inside the project like this: os.path.join(PROJECT_ROOT, ...)
import os
import datetime

PROJECT_ROOT = os.path.realpath(
    os.path.join(
        os.path.dirname(
            os.path.realpath(__file__),
        ),
        '..',
    )
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!ty7fy2%q11dl+!n78#6-u&z3pqzhoj$@7vnn7l=8d$6vvf&-@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_js_reverse',

    'aiot_dashboard.apps.common',
    'aiot_dashboard.apps.db',
    'aiot_dashboard.apps.rooms',
    'aiot_dashboard.apps.power_meters',
    'aiot_dashboard.apps.operations',
    'aiot_dashboard.apps.display',
)

MIDDLEWARE_CLASSES = (
#    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'aiot_dashboard.core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
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

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

WSGI_APPLICATION = 'aiot_dashboard.core.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
    }
}

LANGUAGE_CODE = 'nb-no'
TIME_ZONE = 'Europe/Oslo'

USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'

# PLACEHOLDERS - These need to be obtained dynamically!
SSE_MAX_TIME = datetime.timedelta(minutes=5)
