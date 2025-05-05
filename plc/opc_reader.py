import sys
import pathlib
import os

# Dynamický import projektu
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from opcua import Client
from plc.models import PLC, Sensor, SensorReading


def read_opcua_data(plc_name):
    try:
        plc = PLC.objects.get(name=plc_name)
        if plc.protocol != 'opcua':
            print(f"❌ PLC {plc.name} nepodporuje OPC UA.")
            return

        endpoint = f"opc.tcp://{plc.ip_address}:{plc.port}"
        print(f"🔌 Pokus o pripojenie k {endpoint}...")
        client = Client(endpoint)
        client.connect()
        print(f"✅ Pripojené k {endpoint}")

        sensors = plc.sensors.all()
        print(f"🔍 Načítaných senzorov: {sensors.count()}")

        for sensor in sensors:
            print(f"➡️ Čítam {sensor.name} (node_id: {sensor.node_id})")
            try:
                node = client.get_node(sensor.node_id)
                value = node.get_value()
                SensorReading.objects.create(sensor=sensor, value=value)
                print(f"💾 Uložené: {sensor.name} = {value}")
            except Exception as e:
                print(f"⚠️ Chyba pri čítaní {sensor.name}: {e}")

        client.disconnect()
        print("🔌 Odpojené od PLC.")

    except Exception as e:
        print(f"❌ Kritická chyba: {e}")


if __name__ == "__main__":
    read_opcua_data("plc_compressor")
