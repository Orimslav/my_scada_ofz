from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from plc.models import Sensor, SensorReading
from plc.serializers import LatestSensorValueSerializer
from django.db.models import Max


class LatestSensorValuesView(APIView):
    def get(self, request):
        latest_data = []
        sensors = Sensor.objects.all()

        for sensor in sensors:
            latest_reading = sensor.readings.order_by('-timestamp').first()
            if latest_reading:
                latest_data.append({
                    'sensor': sensor.name,
                    'value': latest_reading.value,
                    'timestamp': latest_reading.timestamp,
                })

        serializer = LatestSensorValueSerializer(latest_data, many=True)
        return Response(serializer.data)

class SensorHistoryView(APIView):
    def get(self, request, sensor_name):
        try:
            sensor = Sensor.objects.get(name=sensor_name)
        except Sensor.DoesNotExist:
            return Response({'error': 'Sensor not found'}, status=status.HTTP_404_NOT_FOUND)

        since = timezone.now() - timedelta(hours=24)
        readings = SensorReading.objects.filter(sensor=sensor, timestamp__gte=since).order_by('timestamp')

        data = [{'timestamp': r.timestamp, 'value': r.value} for r in readings]
        return Response(data)

