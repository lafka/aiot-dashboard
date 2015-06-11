import json
import time

from django import http
from django.conf import settings
from django.utils import timezone, dateparse
from django.views.generic.base import View

class EventsSseView(View):
    def dispatch(self, request, *args, **kwargs):
        super(EventsSseView, self).dispatch(request, *args, **kwargs)

        self.last_datetime = dateparse.parse_datetime(request.GET['last_datetime'])
        response = http.StreamingHttpResponse(streaming_content=self._iterator(request=request),
                                              content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response

    def _iterator(self, request):
        start = timezone.now()
        while timezone.now() - start < settings.SSE_MAX_TIME:
            data = self._fetch_events()
            yield "data: %s\n" % json.dumps(data)
            yield "\n"

            time.sleep(1)

    def _fetch_events(self):
        now = timezone.now()
        data = self.get_events(self.last_datetime, now)
        self.last_datetime = now
        return data

    def get_events(self, datetime_from, datetime_to):
        raise NotImplementedError()
