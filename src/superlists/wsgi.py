"""
WSGI config for superlists project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

# from django.conf import settings
# from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superlists.settings")


# if settings.DEBUG:
#     # Add middleware to handle static files when using gUnicorn in DEBUG MODE
#     application = StaticFilesHandler(get_wsgi_application())
# else:
#     application = get_wsgi_application()
application = get_wsgi_application()
