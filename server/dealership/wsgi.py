import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealership.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
