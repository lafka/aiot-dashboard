import datetime
import time
import json

from django import http, db
from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.utils import timezone
from aiot_dashboard.apps.db.models import Room


class DisplayView(TemplateView):
    template_name = "display/display.html"


# Base class for server side event update streams.
class SseUpdateView(View):
    last_poll = datetime.datetime(2010, 1, 1)

    def dispatch(self, request):
        response = http.StreamingHttpResponse(streaming_content=self.iterator(request=request), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response

    def iterator(self, request):
        start = timezone.now()
        while timezone.now() - start < settings.SSE_MAX_TIME:
            data = self.get_updates()
            if data:
                yield "data: %s\n" % json.dumps(data)
                yield "\n"

            if settings.DEBUG:
                # Prevents a memory leak on dev
                db.reset_queries()

    def get_updates(self):
        time.sleep(1)
        return None


class StatsSseView(SseUpdateView):
    rooms = []

    def get_updates(self):
        if len(self.rooms) == 0:
            self.rooms = Room.get_active_rooms()

        data = {}
        for room in self.rooms:
            data[room.key] = {
                'name': room.name,
                'occupied': room.is_occupied(),
                'productivity': "%s%%" % room.current_productivity(),
                'deviations': {
                    'temperature': room.deviation_minutes('temperature'),
                    'co2': room.deviation_minutes('co2'),
                    'humidity': room.deviation_minutes('humidity')
                }
            }

        time.sleep(10)
        return data
