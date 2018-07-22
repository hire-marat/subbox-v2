#!/usr/bin/env python
# -*- coding: utf-8 -*-

""""""

import os

__copyright__ = "Copyright (c) 2018 ‮nerB ‮taraM"
__author__ = "‮nerB ‮taraM‭"
__license__ = "MPL-2.0"

# Custom settings


class AlwaysNone(object):
  def __getattr__(self, item):
    return None

try: import private
except ImportError: private = AlwaysNone()

SECRET_KEY = (private.SECRET_KEY
              or "don't share this secret key with anyone")

ALLOWED_HOSTS = private.ALLOWED_HOSTS or ['localhost']

YOUTUBE_API_KEY = private.YOUTUBE_API_KEY or ''

# Standard Django stuff

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = [
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'subs'
]

MIDDLEWARE = [
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cfg.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        # 'django.template.context_processors.debug',
        # 'django.template.context_processors.request',
        # 'django.contrib.auth.context_processors.auth',
        # 'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]

WSGI_APPLICATION = 'cfg.wsgi.application'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.',
    'NAME': '',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
  }
}

_validators = 'django.contrib.auth.password_validation.{}'

AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': _validators.format('UserAttributeSimilarityValidator'),
  },
  {
    'NAME':  _validators.format('MinimumLengthValidator'),
  },
  {
    'NAME':  _validators.format('CommonPasswordValidator'),
  },
  {
    'NAME':  _validators.format('NumericPasswordValidator'),
  },
]

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/stc/'

TEMPLATE_DIRS = (
  'stc/html',
)

SESSION_COOKIE_SECURE = private.SESSION_COOKIE_SECURE or False
SESSION_COOKIE_DOMAIN = private.SESSION_COOKIE_DOMAIN or 'localhost'
CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DEFAULT_URL_SCHEME = 'https'
