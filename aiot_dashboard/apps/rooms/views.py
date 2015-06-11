# coding: utf-8
import json

from django.http.response import HttpResponse
from django.views.generic.base import TemplateView

from aiot_dashboard.apps.db.models import Room
from aiot_dashboard.core.filters import get_datetimes_from_filters
from aiot_dashboard.core.sse import EventsSseView

from .utils import get_events

# Room Overview

class RoomOverviewView(TemplateView):
    template_name = "rooms/overview.html"

def room_overview_state(request):
    data = {}
    room_ids = []

    for room in Room.get_active_rooms():
         if room.key not in room_ids:
             data[room.name] = room.get_latest_room_state()
             room_ids.append(room.key)

    return HttpResponse(json.dumps(data), 'application/json')


# Room View

class RoomView(TemplateView):
    template_name = "rooms/detail.html"

    def get_context_data(self, room_key):
        room = Room.objects.get(key=room_key)
        datetimes_from_filter = get_datetimes_from_filters(self.request)

        events = get_events(room, datetimes_from_filter['from'], datetimes_from_filter['to'])
        last_datetime = datetimes_from_filter['to'].isoformat()

        return  {
            'room_key': json.dumps(room.key),
            'events': json.dumps(events),
            'stream': json.dumps(datetimes_from_filter['stream']),
            'last_datetime': json.dumps(last_datetime),
        }

class RoomEventsSseView(EventsSseView):
    def dispatch(self, request, room_key):
        self.room = Room.objects.get(key=room_key)
        super(RoomEventsSseView, self).dispatch(request)

    def get_events(self, datetime_from, datetime_to):
        return get_events(self.room, datetime_from, datetime_to)
