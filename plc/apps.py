"""
apps.py – Konfigurácia aplikácie 'plc' pre Django projekt SCADA

Tento súbor slúži na registráciu aplikácie 'plc' v rámci Django projektu.
Nastavuje predvolený typ primárneho kľúča a názov aplikácie.
"""

from django.apps import AppConfig


class PlcConfig(AppConfig):
    # Predvolený typ ID pre modely (BigAutoField = veľké celé čísla)
    default_auto_field = 'django.db.models.BigAutoField'

    # Názov aplikácie (musí zodpovedať adresárovej štruktúre)
    name = 'plc'
