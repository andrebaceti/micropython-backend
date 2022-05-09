from django.utils import timezone
from django.db import models
from pumpwood_communication.serializers import PumpWoodJSONEncoder
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.singletons import storage_object, base_path


class MicropythonDescriptionGeoarea(models.Model):
    """Geoarea associated with actuator or sensor."""

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
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='geoarea_set',
        verbose_name="Created by user", help_text="Created by user")
    created_at = models.DateTimeField(
        blank=True, null=False, verbose_name="Created at date/time",
        help_text="Created at date/time")

    class Meta:
        db_table = "variable__geoarea"
        verbose_name = 'Geographic Area'
        verbose_name_plural = 'Geographic Area'

    def __str__(self):
        return f"[{self.pk}] {self.description}"

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        return super(
            MicropythonDescriptionGeoarea, self).save(*args, **kwargs)


class MicropythonDescriptionDevice(models.Model):
    """Experiment team to associate the images."""

    LOOP_INTERVAL_CHOICES = (
        ('SS', 'match seconds'),
        ('MM', 'match minute'),
        ('HH', 'match hours'),
        ('sleep__SS', 'sleep for second(s)'),
    )

    device_id = models.TextField(
        null=False, default="", blank=True, unique=True,
        verbose_name="Device self id",
        help_text="Device self id (usually MAC address)")
    description = models.CharField(
        max_length=154, unique=False, blank=True, null=True,
        verbose_name="Short description",
        help_text="Short description of the device")
    notes = models.TextField(
        null=False, default="", blank=True, verbose_name="Long note",
        help_text="Long note containing other information of the devide")

    dimensions = models.JSONField(
        encoder=PumpWoodJSONEncoder, null=False, default=dict,
        blank=True, verbose_name="Dimentions",
        help_text="Key/values dimention field")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='micropython_device_set',
        verbose_name="Created by user",
        help_text="Created by user")
    created_at = models.DateTimeField(
        blank=True, null=False, verbose_name="Creation date/time",
        help_text="Creation date/time")

    default_geoarea = models.ForeignKey(
        MicropythonDescriptionGeoarea, null=False,
        verbose_name="Default device geoarea",
        help_text="Default device geoarea")

    loop_interval_type = models.CharField(
        max_length=10, choices=LOOP_INTERVAL_CHOICES, null=False,
        verbose_name="Internal loop metric",
        help_text="Metric to determine the internal loop interval.")
    loop_interval_interval = models.Integer(blank=False, null=False)
    parameters = models.JSONField(
        encoder=PumpWoodJSONEncoder, null=False, default=dict,
        blank=True)

    class Meta:
        db_table = "device__description"
        verbose_name = 'Device description'
        verbose_name_plural = 'Devices descriptions'

    def __str__(self):
        return f"[{self.pk}] {self.description}"

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        return super(MicropythonDescriptionDevice, self).save(*args, **kwargs)


def change_path_upload(instance, filename):
    """Set path for image."""
    time_fmt = timezone.now().isoformat()
    return (
        "{base_path}/micropythondevicecode__file/"
        "{time_fmt}__{filename}").format(
        base_path=base_path, time_fmt=time_fmt,
        filename=filename.replace(" ", "_").lower())


class MicropythonDeviceCode(models.Model):
    """Codes to be loaded on the evic."""

    LOOP_INTERVAL_CHOICES = (
        ('main', 'Main loop code'),
        ('package', 'Auxiliary package'),
    )

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

    file = models.FileField(
        null=True, blank=True, upload_to=change_path_upload,
        verbose_name="Code file", help_text="Code file")
    device_set = models.ManyToManyField(
        MicropythonDescriptionDevice, related_name="code_set",
        verbose_name="Association of file to devices",
        help_text="Association of file to devices")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='device_code_set',
        verbose_name="User that created",
        help_text="User that created")
    created_at = models.DateTimeField(
        blank=True, null=False, verbose_name="Creation date/time",
        help_text="Creation date/time")

    class Meta:
        db_table = "code__code"
        verbose_name = 'Device code'
        verbose_name_plural = 'Device codes'

    def __str__(self):
        return f"[{self.pk}] {self.description}"

    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        if not self.id:
            self.created_at = timezone.now()
        return super(MicropythonDeviceCode, self).save(*args, **kwargs)
