# coding: utf-8
import json

from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.views.generic.base import TemplateView

from aiot_dashboard.apps.db.models import Room, RoomType, TsCo2, TsMoist, TsLight, TsTemperature, TsDecibel
from aiot_dashboard.core.filters import get_datetimes_from_filters
from aiot_dashboard.core.sse import EventsSseView, DatetimeEventsSseView
from aiot_dashboard.core.utils import to_epoch_mili

from .filters import get_filter_context

# Room Overview

class RoomOverviewView(TemplateView):
    template_name = "rooms/overview.html"

    def get_context_data(self):
        room_types = RoomType.objects.all()

        filter_context = get_filter_context(self.request)
        events_url = reverse('room_overview_events')
        events_url += '?room_type=%s' % filter_context['room_type']

        return  {
            'events_url': json.dumps(events_url),
            'room_types': room_types,
            'filter_context': filter_context,
        }

class RoomOverviewEventsView(EventsSseView):
    def get_events(self):
        rows = []

        overview_tr_tpl = get_template('rooms/overview_tr.html')

        filter_context = get_filter_context(self.request)

        for room in filter_context['rooms']:
            room_state = room.get_latest_room_state()

            overview_tr_html = overview_tr_tpl.render({
                'room': room,
                'temperature': room_state['temperature'],
                'co2': room_state['co2'],
                'noise': room_state['noise'],
                'humidity': room_state['humidity'],
                'movement': room_state['movement'],
                'light': room_state['light'],
            })

            rows.append(overview_tr_html)

        overview_trs_html = u'\n'.join(rows)
        return [{'overview_trs_html': overview_trs_html}]


# Room Detail

class RoomDetailView(TemplateView):
    template_name = "rooms/detail.html"

    def get_context_data(self, room_key):
        room = Room.objects.get(key=room_key)
        active_filter, filter_dts = get_datetimes_from_filters(self.request)
        events_url = reverse('room_detail_events', args=(room.key,))

        return  {
            'room': room,
            'filter_dts': filter_dts,
            'active_filter': active_filter,
            'events_url': json.dumps(events_url),
        }

class RoomDetailEventsView(DatetimeEventsSseView):
    def dispatch(self, request, room_key):
        self.room = Room.objects.get(key=room_key)
        return super(RoomDetailEventsView, self).dispatch(request)

    def get_events(self, datetime_from, datetime_to):
        map_measurement_type_to_ts_class = {
            'co2': TsCo2,
            'humidity': TsMoist,
            'light': TsLight,
            'temperature': TsTemperature,
            'noise': TsDecibel
        }

        data = []
        for key, cls in map_measurement_type_to_ts_class.items():
            for measure in cls.get_ts_between(datetime_from, datetime_to, self.room.devices.first()):
                data.append({
                    'type': key,
                    'value': measure.value,
                    'epoch': to_epoch_mili(measure.datetime),
                })
        return data
