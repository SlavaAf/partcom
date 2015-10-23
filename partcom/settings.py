#coding: utf-8
"""
Django settings for partcom project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import platform
from django.contrib import messages
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

LOGIN_URL = '/account/auth'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9n2(w-8c^qx_fm8&vi8v_if(62s4go+3(os04_o(_1(ygz=*k3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = platform.node() != 'sitio.kz'

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['partcom.kz', 'www.partcom.kz']

ADMINS = (
    ('spacenergy', 'spaceenergy@yandex.ru'),
    ('Anton', 'anton_malkov@icloud.com'),
    ('Dulat', 'dulatbest@mail.ru'),
    ('slavk0', 'crazzy.dead@gmail.com')
    )

MANAGERS = ADMINS

MESSAGE_TAGS={messages.DEBUG: 'debug',
messages.INFO: 'info',
messages.SUCCESS: 'success',
messages.WARNING: 'warning',
messages.ERROR: 'danger'}


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrap3',
    'south',
    'accounts',
    'catalog',
    'delivery',
    'main',
    'gunicorn',
    'ckeditor',
    'bootstrap_pagination',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'bootstrap_pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'partcom.urls'

WSGI_APPLICATION = 'partcom.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'partcom',
            'USER': 'partcom',
            'PASSWORD': 'Vfcn6569Lfq#TreSas3s6965',
            'HOST': 'localhost',
            'PORT': '',

        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

LANGUAGES = (
    ('ru', 'Русский'),
)

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

CKEDITOR_UPLOAD_PATH = os.path.join('static', "img", 'ck')

CKEDITOR_UPLOAD_PREFIX = STATIC_URL + 'img/ck'

CKEDITOR_UPLOAD_SLUGIFY_FILENAME = True


AUTHENTICATION_BACKENDS = (
    'partcom.backends.Backend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request')


REDIS_SSEQUEUE_CONNECTION_SETTINGS = {
    'location': '127.0.0.1:6379',
    'db': 0,
}

