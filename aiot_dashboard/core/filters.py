import urllib
from datetime import timedelta

from django.utils import timezone

def get_datetimes_from_filters(request):
    """
    Parse chosen filters from request.GET, return period to fetch data from.
    If there is no specified `datetime_to` (e.g. "so far today .."), it should return
    `timezone.now()` instead, and return `stream = True`.

    For convenience, we also give out an `url` acceptable for the EventManager.
    """

    ret = {
        'from': timezone.now() - timedelta(days=1),
        'to': timezone.now(),
        'stream': True,
    }

    url_params = {
        'datetime_from': ret['from'].isoformat(),
        'datetime_to': ret['to'].isoformat()
    }
    if ret['stream']:
        url_params['stream'] = 'true'

    ret['events_url_params'] = urllib.urlencode(url_params)

    return ret

