"""
Django settings for CSCapstone project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd6b0#)^misbim_7%oet2yqz+up9=k0c*6ecr_@ee5as&bm^(=y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'CSCapstoneApp',
    'ProjectsApp',
    'CompaniesApp',
    'AuthenticationApp',
    'GroupsApp',
	'UniversitiesApp',
	'CommentsApp',
    'tinymce',
    'BookmarksApp',
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

ROOT_URLCONF = 'CSCapstone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

WSGI_APPLICATION = 'CSCapstone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

AUTH_USER_MODEL = 'AuthenticationApp.MyUser'

#Use @login_required for functions that require authenticated users
LOGIN_URL = "/login"


#TINY MCE CONFIGURATION
#Modified based on code provided on:
#http://stackoverflow.com/questions/24914661/integrate-tinymce-to-django

STATIC_ROOT = "/"

TINYMCE_JS_URL = os.path.join(STATIC_ROOT, "static/tiny_mce/tiny_mce.js")

TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, "static/tiny_mce")

TINYMCE_JS_URL = os.path.join(STATIC_ROOT,'static/tiny_mce/tiny_mce_src.js')
TINYMCE_DEFAULT_CONFIG = {
    "relative_urls": "false",
    "theme": "advanced",
    "theme_advanced_buttons1":     "formatselect,bold,italic,underline,link,unlink,bullist,undo,code,image",
    "theme_advanced_buttons2": "",
    "theme_advanced_buttons3": "",
    "plugins": "paste",
    "height": "200px",
    "width": "700px",
    'theme_advanced_resizing' : "true",
}

TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True

#BLEACH SETTINGS
#http://stackoverflow.com/questions/6830800/how-to-prevent-xss-attacks-when-i-need-to-render-html-from-a-wysiwyg-editor

BLEACH_VALID_TAGS = ['p', 'b', 'i', 'strike', 'ul', 'li', 'ol', 'br',
                     'span', 'blockquote', 'hr', 'a', 'img', 'strong',
                     'em', 'h1', 'h2', 'h3',]
BLEACH_VALID_ATTRS = {
    'span': ['style', ],
    'p': ['align', ],
    'a': ['href', 'rel'],
    'img': ['src', 'alt', 'style'],
}
BLEACH_VALID_STYLES = ['color', 'cursor', 'float', 'margin']
