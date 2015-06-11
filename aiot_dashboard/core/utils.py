import calendar
import datetime

from django.utils import timezone


def get_today():
    now = timezone.now()
    return datetime.datetime(now.year, now.month, now.day).replace(tzinfo=now.tzinfo)

def to_epoch_mili(dt):
    """Converts Python `datetime` object to an UTC epoch in miliseconds (to be
    used with `flot`)
    """
    return calendar.timegm(dt.timetuple()) * 1000
