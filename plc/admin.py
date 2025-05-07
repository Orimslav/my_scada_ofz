"""
admin.py – Registrácia modelov pre Django admin rozhranie (SCADA backend)

Tento súbor zaregistruje všetky relevantné modely (PLC, Sensor, SensorReading)
do administrátorskeho rozhrania Django, aby bolo možné údaje pohodlne spravovať cez webové UI.
"""

from django.contrib import admin
from .models import PLC, Sensor, SensorReading

# Zaregistruj modely pre admin rozhranie – zobrazia sa v Django administrácii
admin.site.register(PLC)           # riadiace jednotky (napr. Kompresor PLC)
admin.site.register(Sensor)        # senzory (napr. prietok, tlak, teplota)
admin.site.register(SensorReading) # historické merania zo senzorov
