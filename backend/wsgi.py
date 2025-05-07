"""
wsgi.py – WSGI konfigurácia pre nasadenie SCADA backendu

Tento súbor definuje vstupný bod pre WSGI servery (napr. Gunicorn, uWSGI),
ktoré spúšťajú Django aplikáciu v produkčnom prostredí.

Oficiálna dokumentácia:
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Nastavenie základného konfiguračného modulu Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Vytvorenie WSGI aplikácie, ktorú použije server (napr. Gunicorn)
application = get_wsgi_application()
