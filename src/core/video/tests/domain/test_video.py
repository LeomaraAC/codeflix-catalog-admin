from decimal import Decimal

import pytest

from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType, Rating
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

    def test_publish_completed_video_marks_as_published(self):
        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
            published=False,
            rating=Rating.AGE_16,
            categories=set(),
            genres=set(),
            cast_members=set(),
            video=AudioVideoMedia(
                name='john-wick.mp4',
                media_type=MediaType.VIDEO,
                raw_location='videos/john-wick.mp4',
                encoded_location='videos/john-wick-encoded.mp4',
                status=MediaStatus.COMPLETED,
            ),
        )

        video.publish()

        assert video.published is True

    def test_publish_without_video_raises_domain_error_after_marking_as_published(self):
        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
            published=False,
            rating=Rating.AGE_16,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        with pytest.raises(ValueError, match='Video media is required to publish the video'):
            video.publish()

        assert video.published is False

    def test_publish_with_unprocessed_video_raises_domain_error_after_marking_as_published(self):
        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
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
                status=MediaStatus.PROCESSING,
            ),
        )

        with pytest.raises(ValueError, match='Video must be fully processed to be published'):
            video.publish()

        assert video.published is False

    def test_process_video_completed_media_updates_video_and_publishes(self):
        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
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

        video.process_video(MediaStatus.COMPLETED, 'videos/john-wick-encoded.mp4')

        assert video.published is True
        assert video.video == AudioVideoMedia(
            name='john-wick.mp4',
            media_type=MediaType.VIDEO,
            raw_location='videos/john-wick.mp4',
            encoded_location='videos/john-wick-encoded.mp4',
            status=MediaStatus.COMPLETED,
        )

    def test_process_video_failed_media_marks_video_as_error_without_publishing(self):
        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
            published=False,
            rating=Rating.AGE_16,
            categories=set(),
            genres=set(),
            cast_members=set(),
            video=AudioVideoMedia(
                name='john-wick.mp4',
                media_type=MediaType.VIDEO,
                raw_location='videos/john-wick.mp4',
                encoded_location='videos/john-wick-encoded.mp4',
                status=MediaStatus.PROCESSING,
            ),
        )

        video.process_video(MediaStatus.ERROR, 'videos/ignored.mp4')

        assert video.published is False
        assert video.video == AudioVideoMedia(
            name='john-wick.mp4',
            media_type=MediaType.VIDEO,
            raw_location='videos/john-wick.mp4',
            encoded_location='',
            status=MediaStatus.ERROR,
        )

    def test_process_video_without_video_raises_domain_error(self):
        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
            published=False,
            rating=Rating.AGE_16,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        with pytest.raises(ValueError, match='Video media is required to process the video'):
            video.process_video(MediaStatus.COMPLETED, 'videos/john-wick-encoded.mp4')

        assert video.published is False
        assert video.video is None

    def test_process_trailer_completed_media_updates_trailer_without_publishing(self):
        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
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

        video.process_trailer(MediaStatus.COMPLETED, 'videos/john-wick-trailer-encoded.mp4')

        assert video.published is False
        assert video.trailer == AudioVideoMedia(
            name='john-wick-trailer.mp4',
            media_type=MediaType.TRAILER,
            raw_location='videos/john-wick-trailer.mp4',
            encoded_location='videos/john-wick-trailer-encoded.mp4',
            status=MediaStatus.COMPLETED,
        )

    def test_process_trailer_failed_media_marks_trailer_as_error(self):
        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
            published=False,
            rating=Rating.AGE_16,
            categories=set(),
            genres=set(),
            cast_members=set(),
            trailer=AudioVideoMedia(
                name='john-wick-trailer.mp4',
                media_type=MediaType.TRAILER,
                raw_location='videos/john-wick-trailer.mp4',
                encoded_location='videos/john-wick-trailer-encoded.mp4',
                status=MediaStatus.PROCESSING,
            ),
        )

        video.process_trailer(MediaStatus.ERROR, 'videos/ignored.mp4')

        assert video.published is False
        assert video.trailer == AudioVideoMedia(
            name='john-wick-trailer.mp4',
            media_type=MediaType.TRAILER,
            raw_location='videos/john-wick-trailer.mp4',
            encoded_location='',
            status=MediaStatus.ERROR,
        )

    def test_process_trailer_without_trailer_raises_domain_error(self):
        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
            published=False,
            rating=Rating.AGE_16,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        with pytest.raises(ValueError, match='Trailer media is required to process the trailer'):
            video.process_trailer(MediaStatus.COMPLETED, 'videos/john-wick-trailer-encoded.mp4')

        assert video.published is False
        assert video.trailer is None
