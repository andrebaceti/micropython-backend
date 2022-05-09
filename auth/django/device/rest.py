"""View for photo end-point."""
import base64
import datetime
from pumpwood_djangoviews.views import PumpWoodRestService
from experiment.serializers import DescriptionExperimentTeamSerializer
from experiment.models import DescriptionExperimentTeam
from rest_framework.response import Response
from pumpwood_communication.exceptions import PumpWoodForbidden
from core.singletons import (
    storage_object, microservice, microservice__no_login)
from device.models import (
    MicropythonDescriptionGeoarea, MicropythonDescriptionDevice,
    MicropythonDeviceCode)
from device.rest import (
    MicropythonDescriptionGeoareaSerializer,
    MicropythonDescriptionDeviceSerializer,
    MicropythonDeviceCodeSerializer)


class RestMicropythonDescriptionGeoarea(PumpWoodRestService):
    endpoint_description = "Geoarea"
    notes = "Geoarea associated with board, actuator or sensor."

    service_model = MicropythonDescriptionGeoarea
    serializer = MicropythonDescriptionGeoareaSerializer

    storage_object = storage_object
    microservice = microservice

    file_fields = {}
    list_fields = [
        "pk", "model_class", "device_id", 'description', 'notes',
        'dimensions', 'created_by', 'created_at', 'default_geoarea',
        'loop_interval_type', 'loop_interval_interval', 'parameters']

    foreign_keys = {
        "created_by": {"model_class": "User", "many": False},
    }


class RestMicropythonDescriptionDevice(PumpWoodRestService):
    endpoint_description = "Device"
    notes = "Edge device description."

    service_model = MicropythonDescriptionDevice
    serializer = MicropythonDescriptionDeviceSerializer

    storage_object = storage_object
    microservice = microservice

    file_fields = {}
    list_fields = [
        'pk', 'model_class', 'device_id', 'description', 'notes',
        'dimensions', 'created_by', 'created_at', 'default_geoarea',
        'loop_interval_type', 'loop_interval_interval', 'parameters']

    foreign_keys = {
        "created_by": {"model_class": "User", "many": False},
    }


class RestMicropythonDeviceCode(PumpWoodRestService):
    endpoint_description = "Codes"
    notes = "Edge device main codes and packages."

    service_model = MicropythonDeviceCode
    serializer = MicropythonDeviceCodeSerializer

    storage_object = storage_object
    microservice = microservice

    file_fields = {'file': ["py"]}
    list_fields = [
        'pk', 'model_class', 'description', 'notes', 'dimensions', 'file',
        'device_set', 'created_by', 'created_at']
    foreign_keys = {
        "created_by": {"model_class": "User", "many": False},
        "device_set": {
            "model_class": "MicropythonDescriptionDevice", "many": False},
    }
