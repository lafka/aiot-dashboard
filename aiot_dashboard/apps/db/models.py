from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone

class TimeSeriesMixin(object):
    @classmethod
    def get_ts_between(cls, start, end, room):
        device = room.devices.all()[0] #TODO: Remember, there might be multiple devices in a room in the future
        return cls.objects.filter(datetime__gte=start, datetime__lte=end, device_key=device.key)


class Deviations(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key', blank=True, null=True)
    deviation_type = models.TextField()

    class Meta:
        managed = False
        db_table = 'deviations'


class Device(models.Model):
    key = models.TextField(primary_key=True)
    name = models.TextField()
    type = models.TextField()

    class Meta:
        managed = False
        db_table = 'device'


class MapDevicePowerCircuit(models.Model):
    device_key = models.ForeignKey(Device, db_column='device_key')
    power_circuit = models.ForeignKey('PowerCircuit')

    class Meta:
        managed = False
        db_table = 'map_device_power_circuit'


class PowerCircuit(models.Model):
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'power_circuit'


class Room(models.Model):
    key = models.TextField(primary_key=True)
    name = models.TextField()
    room_type = models.ForeignKey('RoomType', blank=True, null=True)
    area = models.DecimalField(max_digits=6, decimal_places=2)
    devices = models.ManyToManyField('Device', through='MapDeviceRoom')

    class Meta:
        managed = False
        db_table = 'room'

    @classmethod
    def get_active_rooms(cls):
        return cls.objects.exclude(devices=None).select_related('room_type').prefetch_related('devices')

    def get_latest_ts(self, cls):
        try:
            return cls.objects.filter(device_key__in=self.devices.all()).order_by('-datetime').first()
        except AttributeError:
            return None

    def is_occupied(self):
        return self.current_manminutes() > 0.0

    def current_manminutes(self):
        ts = self.get_latest_ts(TsPersonsInside)
        if ts:
            return ts.value
        return 0

    def current_productivity(self):
        return int((self.current_manminutes() / self.room_type.manminutes_capacity) * 100)

    def deviation_minutes(self, deviation_type):
        today = timezone.now().replace(hour=0, minute=0, second=0)
        return Deviations.objects.filter(device_key__in=self.devices.all(),
                                         deviation_type=deviation_type,
                                         datetime__gte=today).count()

    def get_latest_room_state(self):
        sensor_map = {
            'co2': TsCo2,
            'temp': TsTemperature,
            'db': TsDecibel,
            'moist': TsMoist,
            'movement': TsMovement,
            'lux': TsLight,
        }

        ret = {}

        for key, klass in sensor_map.items():
            instance = klass.objects.filter(device_key=self.devices.all()[0].key, datetime__gt=(datetime.now() -
                timedelta(hours=1))).latest(field_name='datetime') #TODO: Remember, there might be multiple devices in a room in the future

            ret[key] = instance.value if instance else None

        # todo
        ret['name'] = self.name
        ret['key'] = self.key

        return ret


class MapDeviceRoom(models.Model):
    device_key = models.ForeignKey('Device', db_column='device_key')
    room_key = models.ForeignKey('Room', db_column='room_key')

    class Meta:
        managed = False
        db_table = 'map_device_room'
        unique_together = (('device_key', 'room_key'),)


class RoomType(models.Model):
    description = models.TextField()
    manminutes_capacity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'room_type'


class TsCo2(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_co2'
        ordering = ['-datetime']

class TsDecibel(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_decibel'
        ordering = ['-datetime']


class TsEnergyProductivity(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key', blank=True, null=True)
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_energy_productivity'
        ordering = ['-datetime']


class TsKwh(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_kwh'
        ordering = ['-datetime']


class TsKwm(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_kwm'
        ordering = ['-datetime']


class TsLight(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_light'
        ordering = ['-datetime']


class TsMoist(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_moist'
        ordering = ['-datetime']


class TsMovement(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.BooleanField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_movement'
        ordering = ['-datetime']


class TsPersonsInside(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key', blank=True, null=True)
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_persons_inside'
        ordering = ['-datetime']


class TsPulses(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.IntegerField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_pulses'
        ordering = ['-datetime']


class TsTemperature(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_temperature'
        ordering = ['-datetime']
