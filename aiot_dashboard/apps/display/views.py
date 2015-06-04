import datetime
import time

from django import http, db
from django.conf import settings
from django.views.generic.base import TemplateView, View
from django.utils import timezone
import json
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
    room_poll = []

    def _build_room_poll(self):
        for room in Room.objects.all().only('key'):
            self.room_poll.append([room.key, None])

    def _get_room_data(self, room_key):
        room = Room.objects.get(key=room_key)
        return {
            'name': room.name
        }

    def get_updates(self):
        if len(self.room_poll) == 0:
            self._build_room_poll()

        data = {}
        for i in range(len(self.room_poll)):
            room_key, last_poll = self.room_poll[i]

            # TODO: See if there's an update ... if there is, show it.
            # if the last poll is None show it anyway (also get rid of last_poll, record a hash or something for the record)

            if not last_poll:
                data[room_key] = self._get_room_data(room_key)

                self.room_poll[i][1] = datetime.datetime.now()

        time.sleep(1)
        return data
