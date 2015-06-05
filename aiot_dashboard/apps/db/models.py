from __future__ import unicode_literals

from django.db import models


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


class MapDeviceRoom(models.Model):
    device_key = models.ForeignKey(Device, db_column='device_key')
    room_key = models.ForeignKey('Room', db_column='room_key')

    class Meta:
        managed = False
        db_table = 'map_device_room'
        unique_together = (('device_key', 'room_key'),)


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
        return cls.objects.exclude(devices=None)

    def get_latest_ts(self, cls):
        print cls.objects.filter(device_key__in=self.devices.all()).order_by('-datetime').first().datetime
        return None

    def is_occupied(self):
        ts = self.get_latest_ts(TsPersonsInside)
        return False

class RoomType(models.Model):
    description = models.TextField()
    manminutes_capacity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'room_type'


class TsCo2(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_co2'


class TsDecibel(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_decibel'


class TsEnergyProductivity(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key', blank=True, null=True)
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_energy_productivity'


class TsKwh(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_kwh'


class TsKwm(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_kwm'


class TsLight(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_light'


class TsMoist(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_moist'


class TsMovement(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.BooleanField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_movement'


class TsPersonsInside(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key', blank=True, null=True)
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_persons_inside'


class TsPulses(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.IntegerField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_pulses'


class TsTemperature(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_temperature'
