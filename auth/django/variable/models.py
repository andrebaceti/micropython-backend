from django.utils import timezone
from django.db import models
from pumpwood_communication.serializers import PumpWoodJSONEncoder
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from device.models import (
    MicropythonDescriptionDevice, MicropythonDescriptionGeoarea)


class MicropythonDescriptionSensorMetric(models.Model):
    """Variables colected using sersor at the devices."""

    TYPE_CHOICES = (
        ('bool', 'boolean'),
        ('int', 'integer'),
        ('float', 'float'),
        ('char', 'character'),
    )

    type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, null=False,
        verbose_name="Sensor metric type", help_text="Sensor metric type")
    description = models.CharField(
        max_length=154, unique=False, blank=True, null=True,
        verbose_name="Short description", help_text="Short description")
    notes = models.TextField(
        null=False, default="", blank=True, verbose_name="Long note",
        help_text="Long note")

    dimensions = models.JSONField(
        encoder=PumpWoodJSONEncoder, null=False, default=dict,
        blank=True, verbose_name="Dimentions",
        help_text="Key/values dimention field")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=False,
        blank=True, related_name='sensor_metric_set',
        verbose_name="Created by user", help_text="Created by user")
    created_at = models.DateTimeField(
        blank=True, null=False, verbose_name="Created at date/time",
        help_text="Created at date/time")

    class Meta:
        db_table = "variable__sensor"
        verbose_name = 'Sensor metric'
        verbose_name_plural = 'Sensor metrics'

    def __str__(self):
        return f"[{self.pk}] {self.description}"

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        return super(
            MicropythonDescriptionSensorMetric, self).save(*args, **kwargs)


class MicropythonSensorMap(models.Model):
    """Experiment team to associate the images."""

    device_set = models.ManyToManyField(
        MicropythonDescriptionDevice, related_name="sensor_map_set",
        verbose_name="Devices associated", help_text="Devices associated")

    sensor = models.ForeignKey(
        MicropythonDescriptionSensorMetric, null=False,
        verbose_name="Sensor metric", help_text="Sensor metric")
    geoarea = models.ForeignKey(
        MicropythonDescriptionSensorMetric, null=True, blank=True,
        verbose_name="Geoarea",
        help_text="Geoarea (null use board default geoarea)")
    description = models.CharField(
        max_length=154, unique=False, blank=True, null=True,
        verbose_name="Short description", help_text="Short description")
    notes = models.TextField(
        null=False, default="", blank=True, verbose_name="Long note",
        help_text="Long note")
    dimensions = models.JSONField(
        encoder=PumpWoodJSONEncoder, null=False, default=dict,
        blank=True, verbose_name="Dimentions",
        help_text="Key/values dimention field")

    map = models.JSONField(
        encoder=PumpWoodJSONEncoder, null=False, blank=True, default=dict,
        verbose_name="Dictionary maping board pins to sensors and geoarea",
        help_text="Dictionary maping board pins to sensors and geoarea")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=False,
        blank=True, related_name='sensor_matric_map_set',
        verbose_name="Created by user", help_text="Created by user")
    created_at = models.DateTimeField(
        blank=True, null=False,
        verbose_name="Created at date/time", help_text="Created at date/time")

    class Meta:
        db_table = "variable__sensor_map"
        verbose_name = 'Sensor map to database id'
        verbose_name_plural = 'Sensor maps to database ids'

    def __str__(self):
        return f"[{self.pk}] {self.description}"

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        return super(MicropythonSensorMap, self).save(*args, **kwargs)


class MicropythonDescriptionActuatorMetric(models.Model):
    """Variables used to that actions using the devices."""

    TYPE_CHOICES = (
        ('bool', 'boolean'),
        ('int', 'integer'),
        ('float', 'float'),
        ('char', 'character'),
    )

    type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, null=False,
        verbose_name="Actuator metric type", help_text="Actuator metric type")
    description = models.CharField(
        max_length=154, unique=False, blank=True, null=True,
        verbose_name="Short description", help_text="Short description")
    notes = models.TextField(
        null=False, default="", blank=True, verbose_name="Long note",
        help_text="Long note")
    dimensions = models.JSONField(
        encoder=PumpWoodJSONEncoder, null=False, default=dict,
        blank=True, verbose_name="Dimentions",
        help_text="Key/values dimention field")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=False,
        blank=True, related_name='actuator_metric_set',
        verbose_name="Created by user",
        help_text="Created by user")
    created_at = models.DateTimeField(
        blank=True, null=False, verbose_name="Created at date/time",
        help_text="Created at date/time")

    class Meta:
        db_table = "variable__actuator"
        verbose_name = 'Actuator variable'
        verbose_name_plural = 'Actuator variables'

    def __str__(self):
        return f"[{self.pk}] {self.description}"

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        return super(
            MicropythonDescriptionActuatorMetric, self).save(*args, **kwargs)


class MicropythonActuatorMap(models.Model):
    """Experiment team to associate the images."""

    device_set = models.ManyToManyField(
        MicropythonDescriptionDevice, related_name="actuator_map_set",
        verbose_name="Devices associated", help_text="Devices associated")

    actuator = models.ForeignKey(
        MicropythonDescriptionActuatorMetric, null=False,
        verbose_name="Actuator metric", help_text="Actuator metric")
    geoarea = models.ForeignKey(
        MicropythonDescriptionSensorMetric, null=True, blank=True,
        verbose_name="Geoarea",
        help_text="Geoarea (null use board default geoarea)")

    description = models.CharField(
        max_length=154, unique=False, blank=True, null=True,
        verbose_name="Short description", help_text="Short description")
    notes = models.TextField(
        null=False, default="", blank=True, verbose_name="Long note",
        help_text="Long note")
    dimensions = models.JSONField(
        encoder=PumpWoodJSONEncoder, null=False, default=dict,
        blank=True, verbose_name="Dimentions",
        help_text="Key/values dimention field")

    map = models.JSONField(
        encoder=PumpWoodJSONEncoder, null=False, default=dict,
        blank=True,
        verbose_name="Dictionary maping board pins to sensors and geoarea",
        help_text="Dictionary maping board pins to sensors and geoarea")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=False,
        blank=True, related_name='actuator_metric_map_set',
        verbose_name="Created by user",
        help_text="Created by user")
    created_at = models.DateTimeField(
        blank=True, null=False, verbose_name="Created at date/time",
        help_text="Created at date/time")

    class Meta:
        db_table = "variable__actuator_map"
        verbose_name = 'Actuator map to database id'
        verbose_name_plural = 'Actuator maps to database ids'

    def __str__(self):
        return f"[{self.pk}] {self.description}"

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        return super(MicropythonActuatorMap, self).save(*args, **kwargs)
