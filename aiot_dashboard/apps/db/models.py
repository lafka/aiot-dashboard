from __future__ import unicode_literals

from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.db.models.aggregates import Sum

class TimeSeriesMixin(object):
    @classmethod
    def get_ts_between(cls, start, end, device=None):
        if device:
            return cls.objects.filter(datetime__gte=start, datetime__lt=end, device_key=device.key)
        return cls.objects.filter(datetime__gte=start, datetime__lt=end)

    @classmethod
    def get_all_ts(cls, device=None):
        if device:
            return cls.objects.filter(device_key=device.key)
        return cls.objects.all()


class Deviations(models.Model):
    class DeviationType:
        HUMIDITY = 'moist'
        CO2 = 'co2'
        TEMPERATURE = 'temperature'

    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key', blank=True, null=True)
    deviation_type = models.TextField()

    class Meta:
        managed = False
        db_table = 'deviations'
        ordering = ['datetime']

    @classmethod
    def minutes_for_range(cls, start, end, deviation_types=None):
        qs = cls.objects.filter(datetime__gte=start,
                                datetime__lt=end,
                                device_key__in=Room.get_active_devices())
        if deviation_types:
            qs = qs.filter(deviation_type__in=deviation_types)

        return qs.count()


class Device(models.Model):
    key = models.TextField(primary_key=True)
    name = models.TextField()
    type = models.TextField()

    class Meta:
        managed = False
        db_table = 'device'
        ordering = ['name']

class PowerCircuit(models.Model):
    name = models.TextField()
    devices = models.ManyToManyField('Device', through='MapDevicePowerCircuit')

    class Meta:
        managed = False
        db_table = 'power_circuit'
        ordering = ['name']

    def get_last_kwm(self):
        device = self.devices.first()
        if device:
            measure = device.tskwm_set.latest()
            if measure:
                return measure.value

    def get_last_kwh(self):
        device = self.devices.first()
        if device:
            measure = device.tskwh_set.latest()
            if measure:
                return measure.value

class Room(models.Model):
    key = models.TextField(primary_key=True)
    name = models.TextField()
    room_type = models.ForeignKey('RoomType', blank=True, null=True, related_name='rooms')
    area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    floor = models.IntegerField(default=0)
    devices = models.ManyToManyField('Device', through='MapDeviceRoom')

    class Meta:
        managed = False
        db_table = 'room'
        ordering = ['name']

    @classmethod
    def get_active_rooms(cls):
        return cls.objects.exclude(devices=None).select_related('room_type').prefetch_related('devices')

    @classmethod
    def get_active_devices(cls):
        devices = []
        for room in cls.get_active_rooms():
            for device in room.devices.all():
                devices.append(device)
        return devices

    def get_latest_ts(self, cls):
        # TODO: We should not accept values that's way behind in time.
        #       Generally, we should always think "yes, this is the latest, but it might not be current".
        try:
            return cls.objects.filter(device_key__in=self.devices.all()).latest()
        except AttributeError:
            return None

    def current_manminutes(self):
        ts = self.get_latest_ts(TsPersonsInside)
        if ts:
            return ts.value
        return 0

    def current_productivity(self):
        return int((self.current_manminutes() / self.room_type.manminutes_capacity) * 100)

    def deviation_minutes_today(self, deviation_types):
        today = timezone.now().replace(hour=0, minute=0, second=0)
        return Deviations.objects.filter(device_key__in=self.devices.all(),
                                         deviation_type__in=deviation_types,
                                         datetime__gte=today).count()

    def deviation_minutes_for_range(self, start, end, deviation_types=None):
        qs = Deviations.objects.filter(device_key__in=self.devices.all(),
                                       datetime__gte=start,
                                       datetime__lt=end)
        if deviation_types:
            qs = qs.filter(deviation_type__in=deviation_types)

        return qs.count()

    def get_latest_room_state(self):
        sensor_map = {
            'co2': TsCo2,
            'temperature': TsTemperature,
            'noise': TsDecibel,
            'humidity': TsMoist,
            'movement': TsMovement,
            'light': TsLight,
        }

        ret = {}
        for key, klass in sensor_map.items():
            # TODO: Remember, there might be multiple devices in a room in the future
            instance = klass.objects.filter(device_key=self.devices.first().key,
                                            datetime__gt=(timezone.now() - timedelta(hours=1))).latest()

            ret[key] = instance.value if instance else None
        return ret

    def current_co2(self):
        ts = self.get_latest_ts(TsCo2)
        if ts:
            return ts.value
        return 0

    def current_temperature(self):
        ts = self.get_latest_ts(TsTemperature)
        if ts:
            return ts.value
        return 0

    def current_movement(self):
        ts = self.get_latest_ts(TsMovement)
        if ts:
            return ts.value
        return 0

    def subjective_evaluation(self):
        evaluations = TsSubjectiveEvaluation.get_all_ts(self.devices.first())
        if evaluations.count():
            return sum(evaluation.value for evaluation in evaluations) / len(evaluations)

class RoomType(models.Model):
    description = models.TextField()
    manminutes_capacity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'room_type'
        ordering = ['description']

    def get_active_rooms(self):
        return Room.get_active_rooms().filter(room_type=self)


class MapDeviceRoom(models.Model):
    device_key = models.ForeignKey('Device', db_column='device_key')
    room_key = models.ForeignKey('Room', db_column='room_key')

    class Meta:
        managed = False
        db_table = 'map_device_room'
        unique_together = (('device_key', 'room_key'),)

class MapDevicePowerCircuit(models.Model):
    device_key = models.ForeignKey('Device', db_column='device_key')
    power_circuit = models.ForeignKey('PowerCircuit')

    class Meta:
        managed = False
        db_table = 'map_device_power_circuit'


class TsCo2(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_co2'
        ordering = ['datetime']
        get_latest_by = 'datetime'

class TsDecibel(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_decibel'
        ordering = ['datetime']
        get_latest_by = 'datetime'


class TsEnergyProductivity(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key', blank=True, null=True)
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_energy_productivity'
        ordering = ['datetime']
        get_latest_by = 'datetime'


class TsKwh(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key')
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_kwh'
        ordering = ['datetime']
        get_latest_by = 'datetime'

    @classmethod
    def get_max_record_for_period(cls, start, end):
        return cls.objects.filter(datetime__gte=start,
                                  datetime__lt=end).order_by('-value').first()


class TsKwhNetwork(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(primary_key=True)
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_kwh_network'
        ordering = ['datetime']
        get_latest_by = 'datetime'

    @classmethod
    def get_max_record_for_period(cls, start, end):
        return cls.objects.filter(datetime__gte=start,
                                  datetime__lt=end).order_by('-value').first()


class TsKwm(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key')
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_kwm'
        ordering = ['datetime']
        get_latest_by = 'datetime'


class TsLight(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_light'
        ordering = ['datetime']
        get_latest_by = 'datetime'


class TsMoist(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_moist'
        ordering = ['datetime']
        get_latest_by = 'datetime'


class TsMovement(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key')
    value = models.BooleanField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_movement'
        ordering = ['datetime']
        get_latest_by = 'datetime'


class TsPersonsInside(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key', blank=True, null=True)
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_persons_inside'
        ordering = ['datetime']
        get_latest_by = 'datetime'


class TsPulses(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key')
    value = models.IntegerField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_pulses'
        ordering = ['datetime']
        get_latest_by = 'datetime'


class TsTemperature(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key')
    value = models.FloatField()
    packet_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ts_temperature'
        ordering = ['datetime']
        get_latest_by = 'datetime'

class TsSubjectiveEvaluation(models.Model, TimeSeriesMixin):
    datetime = models.DateTimeField(blank=True, null=True)
    device_key = models.ForeignKey('Device', db_column='device_key', blank=True, null=True)
    value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ts_subjective_evaluation'
        ordering = ['datetime']
        get_latest_by = 'datetime'
