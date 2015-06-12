import json
import time

from django import http
from django.conf import settings
from django.utils import timezone, dateparse
from django.views.generic.base import View

class EventsSseView(View):
    """
    - stream
    """
    def dispatch(self, request, *args, **kwargs):
        self.stream = request.GET.get('stream', None) == 'true'

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

            if not self.stream:
                break

            time.sleep(4)

    def _fetch_events(self):
        return self.get_events()

    def get_events(self):
        raise NotImplementedError()

class DatetimeEventsSseView(EventsSseView):
    """
    - datetime_from
    - datetime_to
    """
    def dispatch(self, request, *args, **kwargs):
        self.initial_datetime_from = dateparse.parse_datetime(request.GET['datetime_from'])
        self.initial_datetime_to = dateparse.parse_datetime(request.GET['datetime_to'])
        self.last_datetime_with_data = self.initial_datetime_to
        self.first = True
        return super(DatetimeEventsSseView, self).dispatch(request, *args, **kwargs)

    def _fetch_events(self):
        if self.first:
            data = self.get_events(self.initial_datetime_from, self.initial_datetime_to)
            self.first = False
            self.last_datetime_with_data = self.initial_datetime_to
        else:
            now = timezone.now()
            data = self.get_events(self.last_datetime_with_data, now)
            if data:
                self.last_datetime_with_data = now
        return data

    def get_events(self, datetime_from, datetime_to):
        raise NotImplementedError()
