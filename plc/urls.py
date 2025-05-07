"""
urls.py – URL smerovanie pre SCADA API (plc aplikácia)

Definuje REST API cesty pre frontend:
- `/latest/` – získa najnovšie hodnoty všetkých senzorov
- `/history/<sensor_name>/` – získa historické dáta pre konkrétny senzor

Tieto cesty sú napojené na pohľady vo `views.py`.
"""

from django.urls import path
from plc.views import LatestSensorValuesView, SensorHistoryView

urlpatterns = [
    # API endpoint na získanie najnovších hodnôt zo všetkých senzorov
    path('latest/', LatestSensorValuesView.as_view(), name='latest-values'),

    # API endpoint na získanie historických dát pre konkrétny senzor (napr. "flowVolume_01")
    path('history/<str:sensor_name>/', SensorHistoryView.as_view(), name='sensor-history'),
]
