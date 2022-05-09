from rest_framework import serializers
from pumpwood_djangoviews.serializers import (
    ClassNameField, CustomNestedSerializer, DynamicFieldsModelSerializer)
from device.models import (
    MicropythonDescriptionGeoarea, MicropythonDescriptionDevice,
    MicropythonDeviceCode)


class MicropythonDescriptionGeoareaSerializer(DynamicFieldsModelSerializer):
    pk = serializers.IntegerField(source='id', allow_null=True, required=False)
    model_class = ClassNameField()

    class Meta:
        model = MicropythonDescriptionGeoarea
        fields = (
            'pk', 'model_class', 'description', 'notes', 'dimensions',
            'created_by', 'created_at', 'geometry')
        read_only_fields = ['created_by', 'created_at']

    def create(self, validated_data):
        validated_data["created_by_id"] = self.context['request'].user.id
        return super(
            MicropythonDescriptionGeoareaSerializer, self).create(
                validated_data)


class MicropythonDescriptionDeviceSerializer(DynamicFieldsModelSerializer):
    pk = serializers.IntegerField(source='id', allow_null=True, required=False)
    model_class = ClassNameField()

    class Meta:
        model = MicropythonDescriptionDevice
        fields = (
            'pk', 'model_class', 'device_id', 'description', 'notes',
            'dimensions', 'created_by', 'created_at', 'default_geoarea',
            'loop_interval_type', 'loop_interval_interval', 'parameters')
        read_only_fields = ['created_by', 'created_at']

    def create(self, validated_data):
        validated_data["created_by_id"] = self.context['request'].user.id
        return super(
            MicropythonDescriptionDeviceSerializer, self).create(
                validated_data)


class MicropythonDeviceCodeSerializer(DynamicFieldsModelSerializer):
    pk = serializers.IntegerField(source='id', allow_null=True, required=False)
    model_class = ClassNameField()

    class Meta:
        model = MicropythonDeviceCode
        fields = (
            'pk', 'model_class', 'description', 'notes', 'dimensions',
            'file', 'device_set', 'created_by', 'created_at')
        read_only_fields = ['created_by', 'created_at']

    def create(self, validated_data):
        validated_data["created_by_id"] = self.context['request'].user.id
        return super(
            MicropythonDeviceCodeSerializer, self).create(
                validated_data)
