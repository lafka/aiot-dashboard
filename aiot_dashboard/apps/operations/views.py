import datetime
import math

from django.utils import timezone
from django.db.models.aggregates import Avg

from aiot_dashboard.apps.display.views import BimView, DataSseView
from aiot_dashboard.apps.db.models import TsKwm


class OperationsView(BimView):
    template_name = "operations/operations.html"


class OperationsSseView(DataSseView):
    def _get_current_kwh_for_current_period(self):
        now = timezone.now()
        start = datetime.datetime(now.year, now.month, now.day, now.hour).replace(tzinfo=now.tzinfo)

        if (now - start).total_seconds() < 600:
            start = now - datetime.timedelta(minutes=10)

        total = TsKwm.objects.filter(datetime__gte=start, datetime__lte=now).aggregate(Avg('value'))['value__avg']
        return math.ceil(total * 60) if total else 0
