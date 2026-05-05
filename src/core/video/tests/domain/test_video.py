from decimal import Decimal

import pytest

from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video


class TestVideo:
    def test_title_must_have_less_than_255_characters(self):
        long_title = 'a' * 256
        with pytest.raises(ValueError, match='Title cannot be longer than 255 characters'):
            Video(title=long_title, description='', launch_year=2000, duration=Decimal(0), published=True, rating=Rating.L,
                  categories=set(), genres=set(), cast_members=set())

    def test_title_cannot_be_empty(self):
        with pytest.raises(ValueError, match='Title cannot be empty'):
            Video(title='', description='', launch_year=2000, duration=Decimal(0), published=True, rating=Rating.L,
                  categories=set(), genres=set(), cast_members=set())

    def test_duration_cannot_be_negative(self):
        with pytest.raises(ValueError, match='Duration cannot be negative'):
            Video(title='Title', description='', launch_year=2000, duration=Decimal(-1), published=True, rating=Rating.L,
                  categories=set(), genres=set(), cast_members=set())
