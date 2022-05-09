from django.utils import timezone
from django.db import models
from pumpwood_communication.serializers import PumpWoodJSONEncoder
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from device.models import (
    MicropythonDescriptionDevice, MicropythonDescriptionGeoarea)
from variable.models import (
    MicropythonDescriptionSensor, MicropythonDescriptionActuator)


class MicropythonDatabaseSensor(models.Model):
    """Database for board sensors values."""

    time = models.DateTimeField(
        null=False, verbose_name="Date/time",
        help_text="Date/time of reference")
    device = models.ForeignKey(
        MicropythonDescriptionDevice, null=False,
        verbose_name="Device",
        help_text="Device associated with value")
    geoarea = models.ForeignKey(
        MicropythonDescriptionGeoarea, null=True, blank=True,
        verbose_name="Geoarea", help_text="Geoarea")
    sensor = models.ForeignKey(
        MicropythonDescriptionSensor, null=False,
        verbose_name="Sensor",
        help_text="Sensor associated with value")
    value = models.FloatField(
        null=False, verbose_name="Value",
        help_text="Value associated time/device/sensor")

    created_at = models.DateTimeField(
        blank=True, null=False, verbose_name="Creation Date/Time",
        help_text="Creation Date/Time ")

    class Meta:
        db_table = "database__sensor"
        verbose_name = 'Sensor data'
        verbose_name_plural = 'Sensor data'

    def __str__(self):
        return f"[{self.pk}] {self.description}"

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        return super(MicropythonDatabaseSensor, self).save(*args, **kwargs)


class MicropythonDatabaseActuator(models.Model):
    """Database for board actuator values."""

    device = models.ForeignKey(
        MicropythonDescriptionDevice, null=False, verbose_name="Device",
        help_text="Device associated with value")
    actuator = models.ForeignKey(
        MicropythonDescriptionActuator, null=False, verbose_name="Actuator",
        help_text="Actuator associated with value")
    geoarea = models.ForeignKey(
        MicropythonDescriptionGeoarea, null=True, blank=True,
        verbose_name="Geoarea", help_text="Geoarea associated with value")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=False,
        blank=True, related_name='actuator_database_set',
        verbose_name="Created by user", help_text="Created by user")
    created_at = models.DateTimeField(
        blank=True, null=False, verbose_name="Creation date/time",
        help_text="Creation date/time ")

    asked_at = models.DateTimeField(
        null=False, verbose_name="Time to perform action",
        help_text="Date/time the actuator was asked")
    asked_value = models.FloatField(
        null=False, verbose_name="Value asked for actuator",
        help_text="Value that was asked")

    performed_at = models.DateTimeField(
        blank=True, null=True, verbose_name="Date/time the actuator was set",
        help_text="Actual date/time the actuator was set")
    performed_value = models.FloatField(
        blank=True, null=True, verbose_name="Actual value that was set",
        help_text="Actual value that was set")

    extra_info = models.JSONField(
        encoder=PumpWoodJSONEncoder, null=False, default=dict,
        blank=True, verbose_name="Other information",
        help_text="Other information")

    class Meta:
        db_table = "database__actuator"
        verbose_name = 'Actuator variable'
        verbose_name_plural = 'Actuator variables'

    def __str__(self):
        return f"[{self.pk}] {self.description}"

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        return super(MicropythonDatabaseActuator, self).save(*args, **kwargs)
