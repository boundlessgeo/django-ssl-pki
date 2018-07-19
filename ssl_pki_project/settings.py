# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2018 Boundless Spatial
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################
"""
Django settings for ssl_pki_project project.

Generated by 'django-admin startproject' using Django 1.8.18.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


def str2bool(v):
    if v and len(v) > 0:
        return v.lower() in ("yes", "true", "t", "1")
    else:
        return False


DOCKER_DJANGO = str2bool(os.getenv('DOCKER_DJANGO', 'False'))

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJ_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6h@^49zs=h7gj4$%ob51y_t+r^m^5hi$z+ie7q9v#g7i!zy$#o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', ['*'])


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ordered_model',
    'ssl_pki',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'ssl_pki_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJ_DIR, 'templates')],
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

WSGI_APPLICATION = 'ssl_pki_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
_db_parent_dir = '/tmp' if DOCKER_DJANGO else PROJ_DIR
_db_name = os.getenv('DOCKER_DJANGO_TEST_DB',
                     os.path.join(_db_parent_dir, 'db.sqlite3'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': _db_name,
        'TEST': {
            'NAME': _db_name,
        }

    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# noinspection PyUnresolvedReferences
STATIC_ROOT = '/tmp/static'
STATIC_URL = '/static/'


SITEURL = os.getenv('SITEURL',
                    'http://nginx-pki.boundless.test:8880')
SITE_LOCAL_URL = os.getenv('SITE_LOCAL_URL',
                           'http://django-pki.boundless.test:8808')

_docker_pki_dir = '/code/ssl_pki/tests/files'
_local_pki_dir = os.path.join(BASE_DIR, 'ssl_pki', 'tests', 'files')
PKI_DIRECTORY = os.getenv(
    'PKI_DIRECTORY',
    _docker_pki_dir if DOCKER_DJANGO and os.path.exists(_docker_pki_dir)
    else _local_pki_dir
)

# This mocks proxy routes, like used in GeoNode
PROXY_URL = '/proxy/?url='

# Force max length validation on encrypted password fields
ENFORCE_MAX_LENGTH = 1

# Should always be set to true if we're behind a proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO_PLUS', 'https')

# Logging settings
DJANGO_IGNORED_WARNINGS = {
    'RemovedInDjango18Warning',
    'RemovedInDjango19Warning',
    'RuntimeWarning: DateTimeField',
}


# See: https://stackoverflow.com/a/30716923
def filter_django_warnings(record):
    for ignored in DJANGO_IGNORED_WARNINGS:
        if ignored in record.args[0]:
            return False
    return True


# 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'
DJANGO_LOG_LEVEL = os.getenv('DJANGO_LOG_LEVEL', 'DEBUG')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
                ('%(levelname)s %(asctime)s %(pathname)s %(process)d '
                 '%(thread)d %(message)s'),
        },
    },
    'handlers': {
        'console': {
            'level': DJANGO_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'filters': {
        'ignore_django_warnings': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': filter_django_warnings,
        },
    },
    'loggers': {
        'py.warnings': {
            'handlers': ['console', ],
            'filters': ['ignore_django_warnings', ],
        },
        # 'ssl_pki': {
        #     'handlers': ['console'],
        #     'level': DJANGO_LOG_LEVEL,
        # },
        # 'urllib3': {
        #     'handlers': ['console'],
        #     'level': DJANGO_LOG_LEVEL,
        # },
        # 'requests': {
        #     'handlers': ['console'],
        #     'level': DJANGO_LOG_LEVEL,
        # },
    },
    'root': {
        'handlers': ['console'],
        'level': DJANGO_LOG_LEVEL
    },
}

LOGGING['loggers']['django.db.backends'] = {
    'handlers': ['console'],
    'propagate': False,
    'level': 'WARNING',  # Django SQL logging is too noisy at DEBUG
}
