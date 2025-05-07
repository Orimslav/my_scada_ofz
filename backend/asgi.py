"""
asgi.py – ASGI konfigurácia pre backend SCADA projektu

Tento súbor definuje vstupný bod pre ASGI server (napr. Daphne, Uvicorn),
ktorý umožňuje spúšťať Django v asynchrónnom režime (napr. pre WebSockety).

Používa sa v moderných architektúrach s real-time komunikáciou.
Viac na: https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Nastavenie Django konfiguračného modulu
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Inicializácia ASGI aplikácie
application = get_asgi_application()
