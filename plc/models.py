from django.db import models

# Model pre jedno PLC zariadenie
class PLC(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField()
    protocol = models.CharField(max_length=20, choices=[('opcua', 'OPC UA')])

    def __str__(self):
        return self.name

# Model pre jednotlivé senzory pripojené na PLC
class Sensor(models.Model):
    plc = models.ForeignKey(PLC, related_name='sensors', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    node_id = models.CharField(max_length=255)
    data_type = models.CharField(max_length=50, choices=[
        ('bool', 'Boolean'),
        ('int', 'Integer'),
        ('float', 'Float'),
        ('string', 'String'),
    ])

    def __str__(self):
        return f"{self.plc.name} - {self.name}"

# Historické záznamy zo senzorov
class SensorReading(models.Model):
    sensor = models.ForeignKey(Sensor, related_name='readings', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return f"{self.sensor.name} = {self.value} @ {self.timestamp}"

