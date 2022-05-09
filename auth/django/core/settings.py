"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import os
import sys
from django.core.wsgi import get_wsgi_application
from pumpwood_djangoauth.kong.create_routes import register_auth_kong_objects

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'jet',
    'flat_json_widget',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    # Django Pumpwood Auth Models
    'pumpwood_djangoauth.registration',
    'pumpwood_djangoauth.system',
]

MIDDLEWARE = [
    # CORS
    'corsheaders.middleware.CorsMiddleware',

    # BASIC
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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
WSGI_APPLICATION = 'core.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/admin/micropython-backend-app/static/'
STATIC_ROOT = "../../static_image/static/"

#########################
# Package configuration #
# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'EXCEPTION_HANDLER': (
        'pumpwood_djangoauth.error_handling.custom_exception_handler'
    )
}

# Nose
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--failed', '--stop', '--verbosity=3', '--nocapture']
FIXTURE_DIRS = ('test_data/',)
###########################


#######################
# Load local settings #
#######################
try:
    from core.local_settings import *
except ImportError:
    print('Problemas com o local settings')


#######################
# Register end-points #
#######################
is_cloud_deploy = os.environ.get("CLOUD", "FALSE") == "TRUE"
if is_cloud_deploy:
    if "core.wsgi" in sys.argv:
        print("#########################################")
        print("# Registering API end-points on kong... #")
        print("#########################################")
        get_wsgi_application()

        from pumpwood_djangoauth.system.views import (
            RestKongRoute, RestKongService)
        from pumpwood_djangoauth.registration.views import RestUser
        service_url = os.environ.get("SERVICE_URL")
        auth_static_service = os.environ.get("AUTH_STATIC_SERVICE")

        # Register rest end-points and admin
        register_auth_kong_objects(
            service_url=service_url,
            service_name="micropython-backend-app",
            healthcheck_route="/health-check/micropython-backend-app/",
            service_description="Authentication Microservice",
            service_notes=(
                "Microservice responsible for User's authentication and "
                "general Pumpwood systems end-points."),
            service_dimentions={
                "microservice": "micropython-backend-app",
                "type": "core",
                "function": "authentication"},
            service_icon=None,
            service_extra_info={},
            routes=[{
                "route_url": "/rest/registration/",
                "route_name": "api--registration",
                "route_type": "aux",
                "description": "Registration",
                "notes": (
                    "End-point for login, logout and other Authentication "
                    "functions"),
                "dimentions": {
                    "microservice": "micropython-backend-app",
                    "service_type": "core",
                    "function": "authentication",
                    "endpoint": "registration",
                    "route_type": "aux"},
                "icon": "",
                "extra_info": {}
            }, {
                "route_url": "/rest/pumpwood/",
                "route_name": "api--pumpwood",
                "route_type": "aux",
                "description": "Pumpwood System",
                "notes": (
                    "System related end-points to list Kong routes, and "
                    "dummy-calls"),
                "dimentions": {
                    "microservice": "micropython-backend-app",
                    "service_type": "core",
                    "function": "system",
                    "endpoint": "pumpwood",
                    "route_type": "aux"},
                "icon": "",
                "extra_info": {}
            }, {  # Admin
                "route_url": "/admin/micropython-backend-app/gui/",
                "route_name": "admin--micropython-backend-app",
                "route_type": "admin",
                "description": "Pumpwood Auth Admin",
                "notes": (
                    "Admin for micropython-backend-app microservice."),
                "dimentions": {
                    "microservice": "micropython-backend-app",
                    "service_type": "core",
                    "function": "gui",
                    "route_type": "admin"},
                "icon": "",
                "extra_info": {}
            }],
            viewsets=[RestKongRoute, RestKongService, RestUser])

        register_auth_kong_objects(
            service_url=auth_static_service,
            service_name="pumpwood-auth-static",
            healthcheck_route=None,
            service_description="Authentication Microservice Static Files",
            service_notes=(
                "Static files for Pumpwood Auth Admin"),
            service_dimentions={
                "microservice": "micropython-backend-app",
                "type": "static",
                "function": "authentication"},
            service_icon=None,
            service_extra_info={},
            routes=[{
                # Admin static files
                "route_url": "/admin/micropython-backend-app/static/",
                "route_name": "static--pumpwood-auth",
                "route_type": "static",
                "description": "Pumpwood Auth Admin Static Files",
                "notes": (
                    "Static files for micropython-backend-app microservice admin."),
                "dimentions": {
                    "microservice": "micropython-backend-app",
                    "service_type": "core",
                    "function": "gui",
                    "route_type": "static"},
                "icon": "",
                "extra_info": {}
            }])
