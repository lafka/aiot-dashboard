import datetime
import json
import time

from django import http, db
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.utils import timezone
from django.views.generic.base import TemplateView, View

from aiot_dashboard.apps.devices.models import RoomState, PowerMeterTimeseries, Device

# Dashboard Home

class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        data = TemplateView.get_context_data(self, **kwargs)
        data['token'] = settings.BIMSYNC_TOKEN
        data['update_url'] = reverse('dashboard_updates')
        return data


class UpdateSseView(View):
    last_poll = datetime.datetime(2010, 1, 1)

    def dispatch(self, request):
        response = http.StreamingHttpResponse(streaming_content=self.iterator(request=request), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response

    def _get_new_room_states(self):
        data = []
        room_ids = []
        for rs in RoomState.get_latest_per_room().order_by('-datetime'):
            if rs.room.key not in room_ids:
                room_ids.append(rs.room.key)
                data.append(rs)

        self.last_poll = timezone.now()
        return data

    def iterator(self, request):
        start = timezone.now()
        while timezone.now() - start < settings.SSE_MAX_TIME:
            new_states = self._get_new_room_states()
            for state in new_states:
                yield "data: %s\n" % json.dumps({
                    'room_key': state.room.key,
                    'datetime': state.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    's_co2': state.s_co2,
                    's_db': state.s_db,
                    's_movement': state.s_movement,
                    's_temperature': state.s_temperature,
                    's_moist': state.s_moist,
                    's_light': state.s_light
                })
                yield "\n"
            time.sleep(1)

            if settings.DEBUG:
                # Prevents a memory leak on dev
                db.reset_queries()


# Room Overview

def room_overview_state(request):
    data = []
    room_ids = []
    for rs in RoomState.get_latest_per_room().order_by('-datetime'):
        if rs.room.key not in room_ids:
            data.append({
                'room': rs.room.key,
                'name': rs.room.name,
                'temp': rs.s_temperature,
                'co2': rs.s_co2,
                'db': rs.s_db,
                'lux': rs.s_light,
                'moist': rs.s_moist,
                'movement': 'Y' if rs.s_movement else 'N',
            })
            room_ids.append(rs.room.key)

    data.sort(key=lambda i: i['name'])
    return HttpResponse(json.dumps(data), 'application/json')

class RoomOverviewView(TemplateView):
    template_name = "dashboard_room_overview.html"


# Room View

def room_state(request, room_id):
    data = []
    for rs in RoomState.objects.filter(room=room_id).order_by('-datetime')[:10]:
        data.append({
            'temp': rs.s_temperature,
            'co2': rs.s_co2,
            'db': rs.s_db,
            'lux': rs.s_light,
            'moist': rs.s_moist,
            'movement': 'Y' if rs.s_movement else 'N',
            'datetime': str(rs.datetime),
        })

    return HttpResponse(json.dumps(data), 'application/json')

class RoomView(TemplateView):
    template_name = "dashboard_room.html"

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return self._get_ajax_data()
        return TemplateView.get(self, request, *args, **kwargs)


# Room Overview

def power_meter_overview_state(request):
    data = []
    for device in Device.objects.filter(type='power-meter').order_by('name'):
        pulses = 0
        data.append({
            'name': device.name,
            'pulses': pulses,
        })
    return HttpResponse(json.dumps(data), 'application/json')

class PowerMeterOverviewView(TemplateView):
    template_name = "dashboard_power_meter_overview.html"
