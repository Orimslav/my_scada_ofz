"""
opc_reader.py – OPC UA klient pre čítanie dát z PLC a zápis do databázy

Tento skript slúži na pripojenie sa k PLC zariadeniam cez protokol OPC UA, načítanie aktuálnych
hodnôt senzorov a uloženie týchto hodnôt do databázy pomocou Django ORM.

Použitie:
$ python opc_reader.py

Predpokladá, že PLC je definované v databáze a má priradené senzory s node_id.
"""

import sys
import pathlib
import os

# Dynamická inicializácia Django prostredia pre skriptový beh mimo servera
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from opcua import Client
from plc.models import PLC, Sensor, SensorReading


def read_opcua_data(plc_name):
    """
    Pripojí sa k zvolenému PLC (ak používa OPC UA), načíta dáta zo senzorov
    a uloží ich ako nové záznamy do databázy.

    Argumenty:
    - plc_name: názov PLC (záznam v databáze)
    """
    try:
        plc = PLC.objects.get(name=plc_name)

        # Kontrola, či PLC používa OPC UA protokol
        if plc.protocol != 'opcua':
            print(f"❌ PLC {plc.name} nepodporuje OPC UA.")
            return

        # Zostavenie endpointu a pripojenie klienta
        endpoint = f"opc.tcp://{plc.ip_address}:{plc.port}"
        print(f"🔌 Pokus o pripojenie k {endpoint}...")
        client = Client(endpoint)
        client.connect()
        print(f"✅ Pripojené k {endpoint}")

        # Načítanie senzorov priradených k PLC
        sensors = plc.sensors.all()
        print(f"🔍 Načítaných senzorov: {sensors.count()}")

        for sensor in sensors:
            print(f"➡️ Čítam {sensor.name} (node_id: {sensor.node_id})")
            try:
                node = client.get_node(sensor.node_id)
                value = node.get_value()

                # Uloženie hodnoty do databázy
                SensorReading.objects.create(sensor=sensor, value=value)
                print(f"💾 Uložené: {sensor.name} = {value}")
            except Exception as e:
                print(f"⚠️ Chyba pri čítaní {sensor.name}: {e}")

        # Odpojenie klienta
        client.disconnect()
        print("🔌 Odpojené od PLC.")

    except Exception as e:
        print(f"❌ Kritická chyba: {e}")


# Manuálne spustenie skriptu (napr. pri testovaní alebo CRON úlohe)
if __name__ == "__main__":
    read_opcua_data("plc_compressor")
