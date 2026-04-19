from rest_framework import serializers

from src.django_project._shared.serializers import ListOutputMetaSerializer


class CategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class ListCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(many=True)
    meta = ListOutputMetaSerializer()


class RetrieveCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(source='*')


class RetrieveCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class CreateCategoryRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False, default=True)


class CreateCategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class DeleteCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class PartialUpdateCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False, required=False)
    description = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
