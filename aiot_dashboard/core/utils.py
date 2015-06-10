import datetime

from django.utils import timezone


def get_today():
    now = timezone.now()
    return datetime.datetime(now.year, now.month, now.day).replace(tzinfo=now.tzinfo)
