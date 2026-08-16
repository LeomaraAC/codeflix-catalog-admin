from decimal import Decimal

import pytest
from django.db import models

from src.core.video.domain.value_objects import Rating
from src.django_project.video_app.models import AudioVideoMedia, ImageMedia, Video


@pytest.mark.parametrize(
    ("field_name", "related_model", "related_name"),
    [
        ("thumbnail", ImageMedia, "video_thumbnail"),
        ("thumbnail_half", ImageMedia, "video_thumbnail_half"),
        ("trailer", AudioVideoMedia, "video_trailer"),
        ("video", AudioVideoMedia, "video_media"),
    ],
)
def test_media_relationship_configuration(field_name, related_model, related_name) -> None:
    field = Video._meta.get_field(field_name)

    assert isinstance(field, models.OneToOneField)
    assert field.related_model is related_model
    assert field.null is True
    assert field.blank is True
    assert field.unique is True
    assert field.remote_field.on_delete is models.SET_NULL
    assert field.remote_field.related_name == related_name


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("field_name", "related_model", "related_name", "media_data"),
    [
        (
            "thumbnail",
            ImageMedia,
            "video_thumbnail",
            {"name": "thumbnail.jpg", "raw_location": "videos/thumbnail.jpg"},
        ),
        (
            "thumbnail_half",
            ImageMedia,
            "video_thumbnail_half",
            {"name": "thumbnail-half.jpg", "raw_location": "videos/thumbnail-half.jpg"},
        ),
        (
            "trailer",
            AudioVideoMedia,
            "video_trailer",
            {"name": "trailer.mp4", "raw_location": "videos/trailer.mp4"},
        ),
        (
            "video",
            AudioVideoMedia,
            "video_media",
            {"name": "video.mp4", "raw_location": "videos/video.mp4"},
        ),
    ],
)
def test_deleting_media_sets_video_relationship_to_null(
    field_name, related_model, related_name, media_data
) -> None:
    media = related_model.objects.create(**media_data)
    video = Video.objects.create(
        title="John Wick",
        description="Action movie",
        launch_year=2014,
        duration=Decimal("120.50"),
        rating=Rating.AGE_16.name,
        **{field_name: media},
    )

    assert getattr(media, related_name) == video

    media.delete()
    video.refresh_from_db()

    assert getattr(video, field_name) is None
