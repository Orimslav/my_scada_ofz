from django.contrib import admin
from .models import PLC, Sensor, SensorReading

# Zaregistruj modely pre admin rozhranie
admin.site.register(PLC)
admin.site.register(Sensor)
admin.site.register(SensorReading)

