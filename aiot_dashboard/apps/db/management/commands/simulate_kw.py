import datetime

from django.core.management.base import BaseCommand

from aiot_dashboard.apps.db.models import TsPulses, TsKwm, TsKwh

class Command(BaseCommand):
    help = 'Adds data to the ts_kwm and ts_kwh views calculated from ts_pulses'

    def handle(self, *args, **options):
        try:
            last_update = TsKwm.objects.all().order_by('-datetime')[0].datetime
            qs = TsPulses.objects.filter(datetime__gte=last_update)
        except IndexError:
            last_update = None
            qs = TsPulses.objects.all()

        for rec in qs:
            if TsKwm.objects.filter(datetime=rec.datetime,
                                    device_key=rec.device_key).count() == 0:
                TsKwm(datetime=rec.datetime,
                      device_key=rec.device_key,
                      value=rec.value / 1000).save()

        self._update_kwh(last_update)

    def _update_kwh(self, last_update):
        if last_update:
            qs = TsKwm.objects.filter(datetime__gte=last_update)
            TsKwh.objects.filter(datetime__gte=last_update).update(value=0)
        else:
            qs = TsKwm.objects.all()
            TsKwh.objects.all().update(value=0)

        for rec in qs.order_by('datetime'):
            hour = datetime.datetime(rec.datetime.year, rec.datetime.month, rec.datetime.day, rec.datetime.hour)
            kwh, _ = TsKwh.objects.get_or_create(device_key=rec.device_key,
                                                 datetime=hour)
            kwh.value += rec.value
            kwh.save()

