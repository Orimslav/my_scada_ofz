from django.core.management.base import BaseCommand
from plc.opc_reader import read_opcua_data

class Command(BaseCommand):
    help = 'Načíta dáta z PLC a uloží ich do databázy'

    def handle(self, *args, **kwargs):
        read_opcua_data("plc_compressor")
