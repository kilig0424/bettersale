"""
Django settings for bettersale project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DB_PASSWORD = config('DB_PASSWORD')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SESSION_COOKIE_AGE。这是一个表示会话超时时间的秒数。
# 当用户在这段时间内没有任何活动（即没有发送任何请求）时，Django会自动结束会话。
SESSION_COOKIE_AGE = 30 * 60  # 30 minutes

# 如果你想让会话在固定的时间后超时，不论用户是否在活动，你可以添加以下设置：
# SESSION_SAVE_EVERY_REQUEST = True



ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
     'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'rest_framework',
    'shops',
    'payments',
    'data_collection'
]

SUIT_CONFIG = {
   # header
   'ADMIN_NAME': 'Django Suit',
   'HEADER_DATE_FORMAT': 'l, j. F Y',
   'HEADER_TIME_FORMAT': 'H:i',

   # forms
   'SHOW_REQUIRED_ASTERISK': True,  # Default True
   'CONFIRM_UNSAVED_CHANGES': True, # Default True

   # menu
   'SEARCH_URL': '/admin/auth/user/',
   'MENU_ICONS': {
      'auth': 'icon-lock',
      'auth.user': 'icon-user',
   },
   'MENU_OPEN_FIRST_CHILD': True, # Default True
   'MENU_EXCLUDE': ('auth.group',),
   'MENU': (
       'sites',
       {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
       {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
       {'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
   ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bettersale.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 指定模板目录
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

WSGI_APPLICATION = 'bettersale.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bettersale_data',
        'USER': 'root',
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# 如果你希望所有的视图都需要用户认证，你可以在你的settings.py文件中添加以下设置：
# 如果你有一些视图不需要用户认证，你可以在这些视图中设置:
# from rest_framework.permissions import IsAuthenticated, AllowAny
# permission_classes=[AllowAny]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}


AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
