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

def get_start_of_month(dte):
    now = timezone.localtime(timezone.now())
    return datetime.datetime(now.year, now.month, 1).replace(tzinfo=now.tzinfo)


def to_epoch_mili(dt):
    """Converts Python `datetime` object to an UTC epoch in miliseconds (to be
    used with `flot`)
    """
    dt = timezone.localtime(dt)
    return calendar.timegm(dt.timetuple()) * 1000

def widen_or_clamp_series(series, start_epoch, end_epoch):
    if not series:
        return

    series[0][0] = start_epoch

    if len(series) == 1:
        series.append([end_epoch, series[0][1]])
    else:
        series[-1][0] = end_epoch
