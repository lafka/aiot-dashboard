from aiot_dashboard.apps.db.models import TsKwm, TsKwh
from aiot_dashboard.core.utils import to_epoch_mili

def get_events(power_circuit, datetime_from, datetime_to):
    map_measurement_type_to_ts_class = {
        'kwh': TsKwh,
        'kwm': TsKwm,
    }

    data = []
    for key, cls in map_measurement_type_to_ts_class.items():
        for measure in cls.get_ts_between(datetime_from, datetime_to, power_circuit.devices.first()):
            data.append({
                'type': key,
                'value': measure.value,
                'epoch': to_epoch_mili(measure.datetime),
            })
    return data
