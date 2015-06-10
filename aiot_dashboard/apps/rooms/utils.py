from datetime import timedelta

from django.utils import timezone

from aiot_dashboard.apps.db.models import TsCo2, TsMoist, TsLight, TsTemperature, TsDecibel
from aiot_dashboard.core.utils import to_epoch_mili

def get_datetimes_from_filters(request):
    # Parse chosen filters from request.GET, return period to fetch data from.
    # If there is no specified `datetime_to` (e.g. "so far today .."), it should return
    # `timezone.now()` instead, and return `stream = True`.
    return {
        'from': timezone.now() - timedelta(hours=1),
        'to': timezone.now(),
        'stream': True,
    }

def get_events(room, datetime_from, datetime_to):
    # Example return:
    # [{'type': 'temperature', 'value': 23.4, 'epoch': 1433862401000},
    #  {'type': 'co2', 'value': 501, 'epoch': 1433862402000}
    #  {'type': 'co2', 'value': 501, 'epoch': 1433862403000}
    # ]

    map_measurement_type_to_ts_class = {
        'co2': TsCo2,
        'moist': TsMoist,
        'lux': TsLight,
        'temp': TsTemperature,
        'db': TsDecibel
    }

    data = []
    for key, cls in map_measurement_type_to_ts_class.items():
        for measure in cls.get_ts_between(datetime_from, datetime_to, room):
            data.append({
                'type': key,
                'value': measure.value,
                'epoch': to_epoch_mili(measure.datetime),
            })
    return data
