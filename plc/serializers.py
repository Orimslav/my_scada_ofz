"""
serializers.py – Serializéry pre SCADA API (Django REST Framework)

Definuje štruktúru a typovanie údajov pre API odpovede.
Používa sa na formátovanie najnovších hodnôt zo senzorov do JSON odpovede.
"""

from rest_framework import serializers

class LatestSensorValueSerializer(serializers.Serializer):
    """
    Serializer pre najnovšiu hodnotu senzora.

    Polia:
    - sensor: názov senzora (napr. "flowVolume_01")
    - value: meraná hodnota (float)
    - timestamp: čas merania (datetime)
    """
    sensor = serializers.CharField()
    value = serializers.FloatField()
    timestamp = serializers.DateTimeField()
