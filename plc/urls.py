from django.urls import path
from plc.views import LatestSensorValuesView, SensorHistoryView

urlpatterns = [
    path('latest/', LatestSensorValuesView.as_view(), name='latest-values'),
    path('history/<str:sensor_name>/', SensorHistoryView.as_view(), name='sensor-history'),
]
