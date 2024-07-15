"""
WSGI config for Marker_Ai project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Marker_Ai.settings')


# Startup script to run compare AI
import compare.startup
application = get_wsgi_application()