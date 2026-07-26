from decimal import Decimal
from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.video.application.exceptions import VideoNotFound
from src.core.video.application.usecase.get_video import GetVideo
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


class TestGetVideo:
    def test_when_video_exists_then_return_output(self):
        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('101.00'),
            published=False,
            rating=Rating.AGE_16,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        mock_repository = create_autospec(VideoRepository)
        mock_repository.get_by_id.return_value = video

        use_case = GetVideo(repository=mock_repository)
        response = use_case.execute(GetVideo.Input(id=video.id))

        assert response == GetVideo.Output(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            published=video.published,
            rating=video.rating,
            categories=video.categories,
            genres=video.genres,
            cast_members=video.cast_members,
        )

    def test_when_video_does_not_exist_then_raise_not_found(self):
        mock_repository = create_autospec(VideoRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetVideo(repository=mock_repository)

        with pytest.raises(VideoNotFound, match=f'Video with id .* not found'):
            use_case.execute(GetVideo.Input(id=uuid4()))