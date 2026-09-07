from decimal import Decimal
from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.video.application.exceptions import InvalidMediaType, MediaNotFound, VideoNotFound
from src.core.video.application.usecase.process_audio_video_media import ProcessAudioVideoMedia
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType, Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


class TestProcessAudioVideoMedia:
    def test_when_processing_video_media_then_updates_video_and_repository(self):
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
            video=AudioVideoMedia(
                name='john-wick.mp4',
                media_type=MediaType.VIDEO,
                raw_location='videos/john-wick.mp4',
                encoded_location='',
                status=MediaStatus.PENDING,
            ),
        )
        mock_repository = create_autospec(VideoRepository)
        mock_repository.get_by_id.return_value = video

        use_case = ProcessAudioVideoMedia(video_repository=mock_repository)

        use_case.execute(
            ProcessAudioVideoMedia.Input(
                video_id=video.id,
                encoded_location='videos/john-wick-encoded.mp4',
                media_type=MediaType.VIDEO,
                status=MediaStatus.COMPLETED,
            )
        )

        mock_repository.get_by_id.assert_called_once_with(video.id)
        mock_repository.update.assert_called_once_with(video)
        assert video.published is True
        assert video.video == AudioVideoMedia(
            name='john-wick.mp4',
            media_type=MediaType.VIDEO,
            raw_location='videos/john-wick.mp4',
            encoded_location='videos/john-wick-encoded.mp4',
            status=MediaStatus.COMPLETED,
        )

    def test_when_processing_trailer_media_then_updates_trailer_and_repository(self):
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
            trailer=AudioVideoMedia(
                name='john-wick-trailer.mp4',
                media_type=MediaType.TRAILER,
                raw_location='videos/john-wick-trailer.mp4',
                encoded_location='',
                status=MediaStatus.PENDING,
            ),
        )
        mock_repository = create_autospec(VideoRepository)
        mock_repository.get_by_id.return_value = video

        use_case = ProcessAudioVideoMedia(video_repository=mock_repository)

        use_case.execute(
            ProcessAudioVideoMedia.Input(
                video_id=video.id,
                encoded_location='videos/john-wick-trailer-encoded.mp4',
                media_type=MediaType.TRAILER,
                status=MediaStatus.COMPLETED,
            )
        )

        mock_repository.get_by_id.assert_called_once_with(video.id)
        mock_repository.update.assert_called_once_with(video)
        assert video.published is False
        assert video.trailer == AudioVideoMedia(
            name='john-wick-trailer.mp4',
            media_type=MediaType.TRAILER,
            raw_location='videos/john-wick-trailer.mp4',
            encoded_location='videos/john-wick-trailer-encoded.mp4',
            status=MediaStatus.COMPLETED,
        )

    def test_when_media_type_is_invalid_then_raise_exception(self):
        mock_repository = create_autospec(VideoRepository)
        use_case = ProcessAudioVideoMedia(video_repository=mock_repository)

        with pytest.raises(InvalidMediaType, match='Invalid media type'):
            use_case.execute(
                ProcessAudioVideoMedia.Input(
                    video_id=uuid4(),
                    encoded_location='videos/john-wick-encoded.mp4',
                    media_type=MediaType.BANNER,
                    status=MediaStatus.COMPLETED,
                )
            )

        mock_repository.get_by_id.assert_not_called()
        mock_repository.update.assert_not_called()

    def test_when_video_does_not_exist_then_raise_exception(self):
        mock_repository = create_autospec(VideoRepository)
        mock_repository.get_by_id.return_value = None
        use_case = ProcessAudioVideoMedia(video_repository=mock_repository)

        with pytest.raises(VideoNotFound, match='Video with ID .* not found'):
            use_case.execute(
                ProcessAudioVideoMedia.Input(
                    video_id=uuid4(),
                    encoded_location='videos/john-wick-encoded.mp4',
                    media_type=MediaType.VIDEO,
                    status=MediaStatus.COMPLETED,
                )
            )

        mock_repository.update.assert_not_called()

    def test_when_video_media_does_not_exist_then_raise_exception(self):
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
        use_case = ProcessAudioVideoMedia(video_repository=mock_repository)

        with pytest.raises(MediaNotFound, match='Video must have a video media to be processed'):
            use_case.execute(
                ProcessAudioVideoMedia.Input(
                    video_id=video.id,
                    encoded_location='videos/john-wick-encoded.mp4',
                    media_type=MediaType.VIDEO,
                    status=MediaStatus.COMPLETED,
                )
            )

        mock_repository.update.assert_not_called()

    def test_when_trailer_media_does_not_exist_then_raise_exception(self):
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
        use_case = ProcessAudioVideoMedia(video_repository=mock_repository)

        with pytest.raises(MediaNotFound, match='Video must have a trailer media to be processed'):
            use_case.execute(
                ProcessAudioVideoMedia.Input(
                    video_id=video.id,
                    encoded_location='videos/john-wick-trailer-encoded.mp4',
                    media_type=MediaType.TRAILER,
                    status=MediaStatus.COMPLETED,
                )
            )

        mock_repository.update.assert_not_called()