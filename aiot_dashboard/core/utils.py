import calendar
import datetime

from django.utils import timezone


def get_today():
    now = timezone.localtime(timezone.now())
    return datetime.datetime(now.year, now.month, now.day).replace(tzinfo=now.tzinfo)

def get_start_of_week(dte):
    while dte.weekday() != 0:
        dte -= datetime.timedelta(days=1)
    return dte

def to_epoch_mili(dt):
    """Converts Python `datetime` object to an UTC epoch in miliseconds (to be
    used with `flot`)
    """
    dt = timezone.localtime(dt)
    return calendar.timegm(dt.timetuple()) * 1000
