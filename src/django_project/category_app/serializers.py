from rest_framework import serializers


class CategoryResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    is_active = serializers.BooleanField()


class ListCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(many=True)


class RetrieveCategoryResponseSerializer(serializers.Serializer):
    data = CategoryResponseSerializer(source='*')


class RetrieveCategoryRequestSerializer(serializers.Serializer):
    id = serializers.UUIDField()
