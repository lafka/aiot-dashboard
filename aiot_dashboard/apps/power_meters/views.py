import json

from django.http.response import HttpResponse
from django.views.generic.base import TemplateView

from aiot_dashboard.apps.db.models import PowerCircuit

# Power Meter Overview

class PowerMetersOverviewView(TemplateView):
    template_name = "power_meters/overview.html"

def power_meters_overview_state(request):
    data = []
    for circuit in PowerCircuit.objects.all():
        last_kwh = circuit.get_last_kwh()
        last_kwm = circuit.get_last_kwm()

        data.append({
            'name': circuit.name,
            'kwm': '%.2f' % last_kwm,
            'kwh': '%.2f' % last_kwh,
        })
    return HttpResponse(json.dumps(data), 'application/json')


# Power Meter View

class PowerMetersDetailView(TemplateView):
    template_name = "power_meters/detail.html"

    def get_context_data(self, device_key):
        return {
            'device_key': device_key,
        }

    def get(self, request, *args, **kwargs):
        return TemplateView.get(self, request, *args, **kwargs)

def power_meters_detail_state(request, device_key):
    # TODO: Finn ut. Husk timezone. Bruk Sse.
    return HttpResponse(json.dumps([]), 'application/json')
