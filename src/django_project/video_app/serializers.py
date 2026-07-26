from rest_framework import serializers

from src.core.video.domain.value_objects import Rating

class RatingTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [(tag.name, tag.name) for tag in Rating]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return Rating[super().to_internal_value(data)]
    
    def to_representation(self, value):
        if isinstance(value, Rating):
            return value.name
        return str(value)


class SetField(serializers.ListField):
    def to_representation(self, value):
        return list(super().to_representation(value))

    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

class CreateVideoInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, allow_blank=False)
    description = serializers.CharField(allow_blank=False)
    launch_year = serializers.IntegerField()
    duration = serializers.DecimalField(max_digits=5, decimal_places=2)
    rating = RatingTypeField()
    categories = SetField(child=serializers.UUIDField())
    genres = SetField(child=serializers.UUIDField())
    cast_members = SetField(child=serializers.UUIDField())

class CreateVideoOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
