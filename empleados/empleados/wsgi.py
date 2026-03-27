"""
WSGI config for empleados project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
import sys

sys.path.append('/opt/render/project/src')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'empleados.empleados.settings')

application = get_wsgi_application()
