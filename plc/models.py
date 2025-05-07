"""
models.py – Dátové modely pre SCADA systém v aplikácii `plc`

Obsahuje tri základné modely:
1. PLC – reprezentuje jedno riadiace zariadenie (napr. Siemens, B&R)
2. Sensor – senzory pripojené k PLC s informáciou o node_id a type dát
3. SensorReading – historické merania, ktoré sa ukladajú do databázy
"""

from django.db import models


# Model pre jedno PLC zariadenie (napr. kompresorový automat)
class PLC(models.Model):
    name = models.CharField(max_length=100, unique=True)  # názov PLC (unikátny identifikátor)
    ip_address = models.GenericIPAddressField()           # IP adresa PLC (napr. 192.168.1.10)
    port = models.IntegerField()                          # Port pre pripojenie (napr. 4840 pre OPC UA)
    protocol = models.CharField(                          # Komunikačný protokol (aktuálne len 'opcua')
        max_length=20,
        choices=[('opcua', 'OPC UA')]
    )

    def __str__(self):
        return self.name


# Model pre jednotlivé senzory pripojené k PLC
class Sensor(models.Model):
    plc = models.ForeignKey(PLC, related_name='sensors', on_delete=models.CASCADE)  # prepojenie na PLC
    name = models.CharField(max_length=100)                                         # názov senzora
    node_id = models.CharField(max_length=255)                                      # OPC UA node ID (napr. "ns=4;s=flow_01")
    data_type = models.CharField(                                                   # typ dát z OPC UA
        max_length=50,
        choices=[
            ('bool', 'Boolean'),
            ('int', 'Integer'),
            ('float', 'Float'),
            ('string', 'String'),
        ]
    )

    def __str__(self):
        return f"{self.plc.name} - {self.name}"


# Model pre historické záznamy zo senzorov
class SensorReading(models.Model):
    sensor = models.ForeignKey(Sensor, related_name='readings', on_delete=models.CASCADE)  # prepojenie na senzor
    timestamp = models.DateTimeField(auto_now_add=True)  # automatický čas uloženia záznamu
    value = models.FloatField()                          # meraná hodnota (ako float)

    def __str__(self):
        return f"{self.sensor.name} = {self.value} @ {self.timestamp}"
