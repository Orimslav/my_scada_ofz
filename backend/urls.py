"""
urls.py – Hlavné smerovanie URL pre Django backend SCADA systému

Tento súbor definuje koreňové smerovanie URL pre celý projekt.
Zahŕňa:
- administráciu Django
- API endpointy z aplikácie `plc`

Viac o routovaní: https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Administrácia Django – prístupná cez /admin/
    path('admin/', admin.site.urls),

    # API smerovanie pre aplikáciu 'plc' – dostupné pod prefixom /api/
    path('api/', include('plc.urls')),
]
