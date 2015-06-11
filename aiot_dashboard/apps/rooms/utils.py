from aiot_dashboard.apps.db.models import TsCo2, TsMoist, TsLight, TsTemperature, TsDecibel
from aiot_dashboard.core.utils import to_epoch_mili

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
        for measure in cls.get_ts_between(datetime_from, datetime_to, room.devices.first()):
            data.append({
                'type': key,
                'value': measure.value,
                'epoch': to_epoch_mili(measure.datetime),
            })
    return data
