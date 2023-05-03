"""
Django settings for subproject: event_manager
"""

import os
from .settings_common import *


# Site config
DOMAIN = SITES['event_manager']['domain']

# Media files (Images)
MEDIA_URL = SITES['event_manager']['media_url']
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JavaScript, Images)
STATIC_URL = SITES['event_manager']['static_url']
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Configurazione URL
ROOT_URLCONF = 'urls.event_manager_urls'



