import json

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from aiot_dashboard.apps.db.models import PowerCircuit
from aiot_dashboard.core.filters import get_datetimes_from_filters
from aiot_dashboard.core.sse import EventsSseView

from .utils import get_events

# Power Meter Overview

class PowerMetersOverviewView(TemplateView):
    template_name = "power_meters/overview.html"

    def get_context_data(self):
        events_url = reverse('power_meters_overview_events') + '?stream=true'
        return  {
            'events_url': json.dumps(events_url),
        }

class PowerMetersOverviewEventsView(EventsSseView):
    def get_events(self):
        data = []
        for circuit in PowerCircuit.objects.all():
            last_kwh = circuit.get_last_kwh()
            last_kwm = circuit.get_last_kwm()

            data.append({
                'name': circuit.name,
                'id': circuit.id,
                'kwm': '%.2f' % last_kwm,
                'kwh': '%.2f' % last_kwh,
            })
        return [data]

# Power Meter View

class PowerMetersDetailView(TemplateView):
    template_name = "power_meters/detail.html"

    def get_context_data(self, power_circuit_id):
        power_circuit = PowerCircuit.objects.get(pk=power_circuit_id)
        datetimes_from_filter = get_datetimes_from_filters(self.request)

        events = get_events(power_circuit, datetimes_from_filter['from'], datetimes_from_filter['to'])
        last_datetime = datetimes_from_filter['to'].isoformat()

        return {
            'power_circuit': power_circuit,
            'events': json.dumps(events),
            'stream': json.dumps(datetimes_from_filter['stream']),
            'last_datetime': json.dumps(last_datetime),
        }

    def get(self, request, *args, **kwargs):
        return TemplateView.get(self, request, *args, **kwargs)

class PowerMetersDetailEventsSseView(EventsSseView):
    def dispatch(self, request, power_circuit_id):
        self.power_circuit = PowerCircuit.objects.get(key=power_circuit_id)
        super(PowerMetersDetailEventsSseView, self).dispatch(request)

    def get_events(self, datetime_from, datetime_to):
        return get_events(self.power_circuit, datetime_from, datetime_to)
