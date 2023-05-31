"""
Django settings for subproject: event_manager
"""

from .settings_all import *
import os.path

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'alansecretkey'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Settings siti
# SITES = {
#     'event_manager': {
#         'domain':           'localhost', 
#         'base_url':         '/',
#         'media_url':        '/',
#         'static_url':       'static/',
#     },
# }

# Database config
DATABASES = {
    'default': {          
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# The ID, as an integer, of the current site in the django_site database table.
# This is used so that application data can hook into specific site(s) and a
# single database can manage content for multiple sites.
# NB: Per default impostiamo il sito 1 altrimenti questo dà problemi nell'uso
#     del Sites framework.
SITE_ID = 1

# Site code (dummy: must be initialized in derived files)
SITE_CODE = ''

AUTH_USER_MODEL = "event_manager.CustomUser" 

# Site config
DOMAIN = 'localhost'

# Media files (Images)
MEDIA_URL = '/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Host permessi
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Configurazione URL
ROOT_URLCONF = 'urls.event_manager_urls'


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
