import json

from django.http.response import HttpResponse
from django.views.generic.base import TemplateView


# Power Meter Overview

class PowerMetersOverviewView(TemplateView):
    template_name = "power_meters/overview.html"

def power_meters_overview_state(request):
    data = []
    
    data.sort(key=lambda i: i['name'])
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
