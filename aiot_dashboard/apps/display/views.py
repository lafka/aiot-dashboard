import datetime
import math

from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.db.models.aggregates import Sum, Avg
from django.views.generic.base import TemplateView

from aiot_dashboard.apps.db.models import Room, PowerCircuit, TsKwm, TsKwh, TsEnergyProductivity, Deviations, TsKwhNetwork
from aiot_dashboard.core.sse import EventsSseView
from aiot_dashboard.core.utils import get_today


class BimView(TemplateView):
    def get_context_data(self, **kwargs):
        data = TemplateView.get_context_data(self, **kwargs)
        data['model_token'] = settings.BIMSYNC_TOKEN
        return data


class DisplayView(BimView):
    template_name = "display/display.html"


class DataSseView(EventsSseView):
    GRAPH_HOUR_START = 7
    GRAPH_HOUR_END = 18

    rooms = []
    last_power = None
    last_current_kwh = None

    def get_events(self):
        if len(self.rooms) == 0:
            self.rooms = Room.get_active_rooms()

        data = self._build_rooms_msg([])
        data = self._build_graph_msg(data)
        data = self._build_current_kwh_msg(data)
        return data

    def _build_rooms_msg(self, data=[]):
        for room in self.rooms:
            data.append({
                'type': 'room',
                'key': room.key,
                'name': room.name,
                'occupied': room.current_movement(),
                'co2': room.current_co2(),
                'temperature': room.current_temperature(),
                'productivity': "%s%%" % room.current_productivity(),
                'quality_index': room.deviation_minutes_today([Deviations.DeviationType.TEMPERATURE,
                                                               Deviations.DeviationType.CO2,
                                                               Deviations.DeviationType.HUMIDITY]),
                'deviations': {
                    'temperature': room.deviation_minutes_today([Deviations.DeviationType.TEMPERATURE]),
                    'co2': room.deviation_minutes_today([Deviations.DeviationType.CO2]),
                    'humidity': room.deviation_minutes_today([Deviations.DeviationType.HUMIDITY])
                }
            })
        return data

    def _build_graph_msg(self, data=[]):
        if not self.last_power or datetime.datetime.utcnow() - self.last_power > datetime.timedelta(minutes=1):
            circuits = []
            for circuit in PowerCircuit.objects.all().prefetch_related('devices'):
                circuits.append({
                    'name': circuit.name,
                    'kwh': self._build_kwh_for_devices(circuit.devices.all()),
                    'productivity': self._build_energy_productivity_for_devices(circuit.devices.all()) # TODO TODO TODO
                })
            data.append({
                'type': 'graph',
                'circuits': circuits,
                'max_month': self._get_max_kwh_for_current_month(),
                'current_kwh': self._build_current_kwh()
            })
            self.last_power = datetime.datetime.utcnow()
        return data

    def _build_current_kwh_msg(self, data=[]):
        if not self.last_current_kwh or (datetime.datetime.utcnow() - self.last_current_kwh) > datetime.timedelta(seconds=10):
            data.append({
                'type': 'current_kwh',
                'data': self._build_current_kwh()
            })
            self.last_power = datetime.datetime.utcnow()
        return data

    def _build_kwh_for_devices(self, devices=None):
        today = get_today()
        data = []

        for h in range(self.GRAPH_HOUR_START, self.GRAPH_HOUR_END):
            dte = today + datetime.timedelta(hours=h)
            qs = TsKwh.objects.filter(datetime__gte=dte,
                                      datetime__lt=dte + datetime.timedelta(hours=1))
            if devices:
                qs = qs.filter(device_key__in=devices)
            data.append([h, self._get_aggregate_sum(qs)])
        return data

    def _build_energy_productivity_for_devices(self, devices): # TODO TODO TODO
        today = get_today()
        data = []

        for h in range(self.GRAPH_HOUR_START, self.GRAPH_HOUR_END):
            dte = today + datetime.timedelta(hours=h)
            qs = TsEnergyProductivity.objects.filter(datetime__gte=dte,
                                                     datetime__lt=dte + datetime.timedelta(hours=1))
            if devices:
                qs = qs.filter(device_key__in=devices)
            data.append([h, self._get_aggregate_avg(qs)])
        return data

    def _get_aggregate(self, qs, func=Sum, key='value__sum'):
        val = qs.aggregate(func('value'))[key]
        if not val:
            val = 0
        return val

    def _get_aggregate_sum(self, qs):
        return self._get_aggregate(qs, Sum, 'value__sum')

    def _get_aggregate_avg(self, qs):
        return self._get_aggregate(qs, Avg, 'value__avg')

    def _build_current_kwh(self):
        return {
            'max': math.ceil(self._get_max_kwh_for_current_month()),
            'current': self._get_current_kwh_for_current_period()
        }

    def _get_max_kwh_for_current_month(self):
        today = get_today()
        month_start = datetime.datetime(today.year, today.month, 1)
        max_kwh = TsKwhNetwork.get_max_record_for_period(month_start, month_start + relativedelta(months=1))
        return max_kwh.value if max_kwh is not None else 0

    def _get_current_kwh_for_current_period(self):
        # Get last 10 TsKwm for each circuit
        # TODO: Not safe if one power meter stops sending measurements.
        total = 0
        for circuit in PowerCircuit.objects.all().prefetch_related('devices'):
            val = TsKwm.objects.filter(id__in=TsKwm.objects.filter(device_key__in=circuit.devices.all())\
                                       .order_by('-datetime')[:10]).aggregate(Avg('value'))['value__avg']
            total += val
        return math.ceil(total * 60) if total else 0
