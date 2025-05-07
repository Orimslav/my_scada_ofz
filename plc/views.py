"""
views.py – API pohľady pre SCADA backend (Django REST Framework)

Tento modul definuje REST API pohľady, ktoré poskytujú:
- najnovšie hodnoty všetkých senzorov
- historické hodnoty pre konkrétny senzor za posledných 7 dní

Používajú sa vo frontende pre vizualizáciu (napr. grafy v Compressor.jsx).
"""

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
    """
    API endpoint: /api/latest/
    
    Vracia najnovšiu hodnotu zo všetkých dostupných senzorov.
    Dátová štruktúra: zoznam objektov obsahujúcich názov senzora, hodnotu a časovú pečiatku.
    """
    def get(self, request):
        latest_data = []  # zoznam pre výsledné dáta
        sensors = Sensor.objects.all()  # získa všetky senzory z databázy

        # nájdi posledné meranie pre každý senzor
        for sensor in sensors:
            latest_reading = sensor.readings.order_by('-timestamp').first()
            if latest_reading:
                latest_data.append({
                    'sensor': sensor.name,
                    'value': latest_reading.value,
                    'timestamp': latest_reading.timestamp,
                })

        # serializuj výstup a vráť ako JSON odpoveď
        serializer = LatestSensorValueSerializer(latest_data, many=True)
        return Response(serializer.data)


class SensorHistoryView(APIView):
    """
    API endpoint: /api/history/<sensor_name>/

    Vracia historické dáta pre zvolený senzor za posledných 7 dní.
    Používa sa pre generovanie grafu vo frontende.
    """
    def get(self, request, sensor_name):
        # kontrola, či senzor existuje
        try:
            sensor = Sensor.objects.get(name=sensor_name)
        except Sensor.DoesNotExist:
            return Response({'error': 'Sensor not found'}, status=status.HTTP_404_NOT_FOUND)

        # určenie rozsahu histórie – posledných 7 dní
        since = timezone.now() - timedelta(days=7)  # možnosť upraviť na napr. timedelta(hours=24)
        
        # získanie všetkých meraní pre daný senzor v danom rozsahu
        readings = SensorReading.objects.filter(sensor=sensor, timestamp__gte=since).order_by('timestamp')

        # formátovanie výstupu do zoznamu slovníkov
        data = [{'timestamp': r.timestamp, 'value': r.value} for r in readings]
        return Response(data)
