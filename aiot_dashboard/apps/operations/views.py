import datetime
import math

from django.db.models.aggregates import Avg
from django.db import connection
from django.utils import timezone

from aiot_dashboard.apps.display.views import BimView, DataSseView
from aiot_dashboard.apps.db.models import TsKwm, TsKwh, PowerCircuit, Room
from aiot_dashboard.core.utils import to_epoch_mili, widen_or_clamp_series, get_start_of_month


class OperationsView(BimView):
    template_name = "operations/operations.html"


class OperationsSseView(DataSseView):
    def _get_current_kwh_for_current_period(self):
        now = timezone.now()
        start = datetime.datetime(now.year, now.month, now.day, now.hour).replace(tzinfo=now.tzinfo)

        if (now - start).total_seconds() < 600:
            start = now - datetime.timedelta(minutes=10)

        total = TsKwm.objects.filter(datetime__gte=start, datetime__lte=now).aggregate(Avg('value'))['value__avg']
        return 4 * math.ceil(total * 60) if total else 0

    def _build_graph_msg(self, data=[]):
        # Only build msg once per minute
        if self.last_power and datetime.datetime.utcnow() - self.last_power > datetime.timedelta(minutes=1):
            return data

        start, end = self.time_range
        if self.use_current:
            end = timezone.now()

        min_epoch = None
        max_epoch = None

        circuits = []
        for circuit in PowerCircuit.objects.all().prefetch_related('devices'):
            series = []
            for instance in TsKwh.get_ts_between(start, end, device=circuit.devices.first()):
                series.append([to_epoch_mili(instance.datetime), instance.value])

            circuits.append({
                'name': circuit.name,
                'series': series
            })

            circuit_min_epoch = min(row[0] for row in series)
            circuit_max_epoch = max(row[0] for row in series)

            min_epoch = circuit_min_epoch if min_epoch is None else min(circuit_min_epoch, min_epoch)
            max_epoch = circuit_max_epoch if max_epoch is None else max(circuit_max_epoch, max_epoch)

        start_month = get_start_of_month(start)
        max_month_series = self._get_max_kwh_for_time_range(start_month, end)
        widen_or_clamp_series(max_month_series, min_epoch, max_epoch)

        data.append({
            'type': 'graph',
            'circuits': circuits,
            'max_month': {
                'series': max_month_series
            },
            'deviations': self._build_room_deviations()
        })

        self.last_power = datetime.datetime.utcnow()
        return data

    def _build_room_deviations(self):
        start, end = self.time_range
        if self.use_current:
            end = timezone.now()

        return {
            'total': self._get_total_deviations(start, end),
            'rooms': self._get_room_deviations(start, end)
        }

    def _get_max_kwh_for_time_range(self, start, end):
        series = []

        with connection.cursor() as cur:
            cur.execute("""
                SELECT date_trunc('month', datetime) AS dt_month, MAX(value) AS value
                FROM ts_kwh_network
                WHERE datetime BETWEEN %(start)s AND %(end)s
                GROUP BY dt_month
                ORDER BY dt_month
            """, {
                'start': start,
                'end': end,
            })

            for row in cur.fetchall():
                series.append([to_epoch_mili(row[0]), row[1]])

        return series

    def _get_room_deviations(self, start, end):
        series = []

        for room in Room.get_active_rooms():
            room_deviations = room.deviation_minutes_for_range(start, end)
            series.append([room.name, room_deviations])

        return series

    def _get_total_deviations(self, start, end):
        series = []

        with connection.cursor() as cur:
            cur.execute("""
                SELECT date_trunc('hour', datetime) AS dt_hour, COUNT(*) AS value
                FROM deviations
                WHERE datetime BETWEEN %(start)s AND %(end)s
                GROUP BY dt_hour
                ORDER BY dt_hour
            """, {
                'start': start,
                'end': end,
            })

            for row in cur.fetchall():
                series.append([to_epoch_mili(row[0]), row[1]])

        return series
