"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# for heroku
import django_heroku

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@5zf*#sex75=l3xsx4z%wi8!#-p@ij8df&)$4j1tmith(rl*e%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# avoid going to /accounts/profile/ by default
LOGIN_REDIRECT_URL = 'index'

# Application definition

INSTALLED_APPS = [
    'background_task',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_gotolong.amfi',
    'django_gotolong.bhav',
    'django_gotolong.broker.icidir.imf',
    'django_gotolong.broker.icidir.isum',
    'django_gotolong.broker.icidir.itxn',
    'django_gotolong.broker.zerodha.zsum',
    'django_gotolong.broker.zerodha.ztxn',
    'django_gotolong.corpact',
    'django_gotolong.bstmtdiv',
    'django_gotolong.dbstat',
    'django_gotolong.dematsum',
    'django_gotolong.demattxn',
    'django_gotolong.dividend',
    'django_gotolong.fof',
    'django_gotolong.fofeti',
    'django_gotolong.fratio',
    'django_gotolong.ftwhl',
    'django_gotolong.gfundareco',
    'django_gotolong.gweight',
    'django_gotolong.indices',
    'django_gotolong.jsched',
    'django_gotolong.lastrefd',
    'django_gotolong.mfund',
    'django_gotolong.nach',
    'django_gotolong.othinv',
    'django_gotolong.phealth',
    'django_gotolong.screener',
    'django_gotolong.trendlyne',
    'django_gotolong.uploaddoc'
]

# added djdev_panel.middleware.DebugMiddleware for google chrome/developer panel django-developer-panel
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gotolong',
        'USER': 'root',
        'PASSWORD': 'root',
    }
}

# Set DATABASE_URL
# https://github.com/jacobian/dj-database-url
# Engine 	Django Backend 	URL
# PostgreSQL 	django.db.backends.postgresql [1] 	postgres://USER:PASSWORD@HOST:PORT/NAME [2]
# PostGIS 	django.contrib.gis.db.backends.postgis 	postgis://USER:PASSWORD@HOST:PORT/NAME
# MSSQL 	sql_server.pyodbc 	mssql://USER:PASSWORD@HOST:PORT/NAME
# MySQL 	django.db.backends.mysql 	mysql://USER:PASSWORD@HOST:PORT/NAME
# MySQL (GIS) 	django.contrib.gis.db.backends.mysql 	mysqlgis://USER:PASSWORD@HOST:PORT/NAME
# SQLite 	django.db.backends.sqlite3 	sqlite:///PATH [3]
# SpatiaLite 	django.contrib.gis.db.backends.spatialite 	spatialite:///PATH [3]
# Oracle 	django.db.backends.oracle 	oracle://USER:PASSWORD@HOST:PORT/NAME [4]
# Oracle (GIS) 	django.contrib.gis.db.backends.oracle 	oraclegis://USER:PASSWORD@HOST:PORT/NAME
# Redshift 	django_redshift_backend 	redshift://USER:PASSWORD@HOST:PORT/NAME

# note...
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

'''
# disabled auth and password validators
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
'''

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Activate Django Heroku
django_heroku.settings(locals())

# server does not support SSL, but SSL was required
# add ENV=development in the .env file for the below to work:
# we have to crete this variable also
# if os.environ.get('ENV') == 'development':
del DATABASES['default']['OPTIONS']['sslmode']
