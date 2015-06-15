from copy import copy
from datetime import timedelta

from django.utils import timezone

def trunc_day(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def get_datetimes_from_filters(request):
    """
    Parse chosen filters from request.GET, return period to fetch data from.
    If there is no specified `datetime_to` (e.g. "so far today .."), it should return
    `timezone.now()` instead, and return `stream = True`.

    For convenience, we also give out an `url` acceptable for the EventManager.
    """

    now = timezone.now()

    map_time_to_datetimes = {
        'last_4_hours': {
            'from': now - timedelta(hours=4),
            'to': now,
            'stream': True
        },
        'today': {
            'from': trunc_day(now),
            'to': now,
            'stream': True
        },
        'yesterday': {
            'from': trunc_day(now - timedelta(days=1)),
            'to': trunc_day(now),
            'stream': False
        },
        'last_7_days': {
            'from': trunc_day(now - timedelta(days=7)),
            'to': now,
            'stream': False
        },
    }

    time_str =  request.GET.get('time', 'last_7_days')
    ret = copy(map_time_to_datetimes[time_str])

    return time_str, ret
