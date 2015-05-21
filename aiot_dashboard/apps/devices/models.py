from __future__ import unicode_literals

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
