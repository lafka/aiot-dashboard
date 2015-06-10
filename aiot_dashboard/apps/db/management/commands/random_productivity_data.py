import random

from django.core.management.base import BaseCommand

from aiot_dashboard.apps.db.models import TsEnergyProductivity, PowerCircuit
from aiot_dashboard.core.utils import get_today
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generates a bunch of random energy productivity readings'

    def handle(self, *args, **options):
        today = get_today()
        TsEnergyProductivity.objects.filter(datetime__gte=today, datetime__lt=today + timedelta(days=1)).delete()

        circuits = PowerCircuit.objects.all()
        for h in range(7, 18):
            dt = today + timedelta(hours=h)
            for m in range(0, 3):
                dt += timedelta(minutes=m * 15)
                for c in circuits:
                    for d in c.devices.all():
                        TsEnergyProductivity(device_key=d,
                                             datetime=dt,
                                             value=random.randint(0, 101)).save()
