# coding: utf-8
import json
import time

from django import http, db
from django.conf import settings
from django.http.response import HttpResponse
from django.utils import timezone, dateparse
from django.views.generic.base import TemplateView, View

from aiot_dashboard.apps.db.models import Room

from .utils import get_events, get_datetimes_from_filters

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

class RoomEventsSseView(View):
    def dispatch(self, request, room_key):
        self.last_datetime = dateparse.parse_datetime(request.GET['last_datetime'])
        self.room = Room.objects.get(key=room_key)

        response = http.StreamingHttpResponse(streaming_content=self.iterator(request=request),
                                              content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response

    def iterator(self, request):
        start = timezone.now()
        while timezone.now() - start < settings.SSE_MAX_TIME:
            data = self.get_updates()
            if data:
                yield "data: %s\n" % json.dumps(data)
                yield "\n"

            time.sleep(1)

            if settings.DEBUG:
                # Prevents a memory leak on dev
                db.reset_queries()

    def get_updates(self):
        now = timezone.now()
        data = get_events(self.room, self.last_datetime, now)
        self.last_datetime = now
        return data
