# coding: utf-8
import json

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from aiot_dashboard.apps.db.models import Room, RoomType, TsCo2, TsMoist, TsLight, TsTemperature, TsDecibel
from aiot_dashboard.core.filters import get_datetimes_from_filters
from aiot_dashboard.core.sse import EventsSseView, DatetimeEventsSseView
from aiot_dashboard.core.utils import to_epoch_mili

# Room Overview

class RoomOverviewView(TemplateView):
    template_name = "rooms/overview.html"

    def get_context_data(self):
        events_url = reverse('room_overview_events')
        room_types = RoomType.objects.all()

        return  {
            'events_url': json.dumps(events_url),
            'room_types': room_types,
        }

class RoomOverviewEventsView(EventsSseView):
    def get_events(self):
        data = []

        for room in Room.get_active_rooms():
            room_state = room.get_latest_room_state()
            room_state['name'] = room.name
            room_state['url'] = reverse('room_detail', args=(room.key,))
            data.append(room_state)

        return [data]


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
