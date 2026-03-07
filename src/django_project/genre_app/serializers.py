from rest_framework import serializers


class SetField(serializers.ListField):
    def to_representation(self, value):
        return list(super().to_representation(value))

    def to_internal_value(self, data):
        return set(super().to_internal_value(data))


class GenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())

class ListGenreOutputSerializer(serializers.Serializer):
    data = GenreOutputSerializer(many=True)

class CreateGenreInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False)
    is_active = serializers.BooleanField(required=False, default=True)
    category_ids = SetField(child=serializers.UUIDField())

class CreateGenreOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class DeleteGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class UpdateGenreInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255, allow_blank=False, required=False)
    is_active = serializers.BooleanField(required=False)
    category_ids = SetField(child=serializers.UUIDField(), required=False)
