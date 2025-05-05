from rest_framework import serializers

class LatestSensorValueSerializer(serializers.Serializer):
    sensor = serializers.CharField()
    value = serializers.FloatField()
    timestamp = serializers.DateTimeField()
