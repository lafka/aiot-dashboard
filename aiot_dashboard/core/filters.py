from datetime import timedelta

from django.utils import timezone

def get_datetimes_from_filters(request):
    # Parse chosen filters from request.GET, return period to fetch data from.
    # If there is no specified `datetime_to` (e.g. "so far today .."), it should return
    # `timezone.now()` instead, and return `stream = True`.
    return {
        'from': timezone.now() - timedelta(days=1),
        'to': timezone.now(),
        'stream': True,
    }

