from __future__ import unicode_literals

from django.db import models


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
        unique_together = (('device_key', 'power_circuit'),)


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
    type = models.TextField()

    class Meta:
        managed = False
        db_table = 'room'


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


class TsPulses(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey(Device, db_column='device_key')
    value = models.FloatField()
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
