"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
import traceback
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

try:
    application = get_wsgi_application()
except Exception:
    # Print traceback to browser for debugging
    def application(environ, start_response):
        start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'text/plain')])
        return [traceback.format_exc().encode('utf-8')]
