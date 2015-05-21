from __future__ import unicode_literals
from collections import OrderedDict
from datetime import datetime, timedelta

from django.db import models, connection


class Device(models.Model):
    key = models.TextField(primary_key=True)
    room = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device'


class Room(models.Model):
    key = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room'


class RoomState(models.Model):
    id = models.IntegerField(primary_key=True)
    datetime = models.DateTimeField(blank=True, null=True)
    room = models.ForeignKey(Room, db_column='room', blank=True, null=True)
    s_co2 = models.IntegerField(blank=True, null=True)
    s_db = models.IntegerField(blank=True, null=True)
    s_movement = models.NullBooleanField()
    s_temperature = models.IntegerField(blank=True, null=True)
    s_moist = models.IntegerField(blank=True, null=True)
    s_light = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_state'

    @classmethod
    def get_latest_per_room(cls):
        cursor = connection.cursor()
        cursor.execute('SELECT max(datetime) FROM room_state GROUP BY room')
        datetimes = [row[0] for row in cursor.fetchall()]
        cursor.close()

        return cls.objects.filter(datetime__in=datetimes)

class PowerMeterTimeseries(models.Model):
    id = models.IntegerField(primary_key=True)
    device = models.ForeignKey(Device, db_column='device_key')
    datetime = models.DateTimeField()
    pulses = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'power_meter_timeseries'

    @classmethod
    def get_latest_kwm(cls, device):
        last_two = cls.objects.filter(device=device).order_by('-datetime')[:2]

        if last_two.count() != 2:
            return None

        last, next_to_last = last_two
        time_diff = last.datetime - next_to_last.datetime

        multiplier = 60 / time_diff.total_seconds()
        calibration_factor = 10000.0
        return int(last.pulses * multiplier / calibration_factor)

    @classmethod
    def get_latest_kwh(cls, device):
        one_hour_ago = datetime.now() - timedelta(hours=1)
        measures = list(cls.objects.filter(device=device, datetime__gt=one_hour_ago).order_by('-datetime'))

        if len(measures) < 2:
            return

        total_pulses = sum(measure.pulses for measure in measures)
        time_diff = measures[0].datetime - measures[-1].datetime
        calibration_factor = 10000.0
        return int((total_pulses / calibration_factor) * (3600 / time_diff.total_seconds()))

    @classmethod
    def get_kwh_timeseries(cls, device, from_datetime, to_datetime):
        kwh_per_hour = OrderedDict()
        datetime_it = from_datetime

        while datetime_it <= to_datetime:
            hour = datetime(datetime_it.year, datetime_it.month, datetime_it.day, datetime_it.hour)
            next_hour = hour + timedelta(hours=1)

            datetime_it = datetime_it + timedelta(hours=1)

            measures = list(cls.objects.filter(device=device, datetime__gte=hour,
                                               datetime__lt=next_hour).order_by('-datetime'))

            if len(measures) < 2:
                continue

            total_pulses = sum(measure.pulses for measure in measures)
            time_diff = measures[0].datetime - measures[-1].datetime
            calibration_factor = 10000.0
            kwh_per_hour[hour] = int((total_pulses / calibration_factor) * (3600 / time_diff.total_seconds()))


        return kwh_per_hour
