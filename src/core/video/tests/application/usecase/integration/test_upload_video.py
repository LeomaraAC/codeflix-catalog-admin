from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core._shared.infrastructure.storage.abstract_storage_service import AbstractStorageService
from src.core.video.application.exceptions import VideoNotFound
from src.core.video.application.usecase.upload_video import UploadVideo
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, Rating
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository

class TestUploadVideo:
    def test_upload_video_media_to_video(self):
        video = Video(
            title='John Wick',
            description='An action movie',
            launch_year=2014,
            duration=101,
            published=True,
            rating=Rating.AGE_16,
            categories=set(),
            genres=set(),
            cast_members=set()
        )

        video_repository = InMemoryVideoRepository(videos=[video])
        mock_storage = create_autospec(AbstractStorageService)

        use_case = UploadVideo(video_repository, mock_storage)

        use_case.execute(
            UploadVideo.Input(
                video_id=video.id,
                file_name='trailer.mp4',
                content=b'video content',
                content_type='video/mp4'
            )
        )

        mock_storage.store.assert_called_once_with(
            file_path=f'videos/{video.id}/trailer.mp4',
            content=b'video content',
            content_type='video/mp4'
        )

        assert video.video == AudioVideoMedia(
            name='trailer.mp4',
            raw_location=f'videos/{video.id}/trailer.mp4',
            encoded_location='',
            status=MediaStatus.PENDING
        )

        assert video_repository.videos[0] == video

        


    def test_when_video_does_not_exist_should_raise_exception(self):
        video_repository = InMemoryVideoRepository(videos=[])
        mock_storage = create_autospec(AbstractStorageService)
        use_case = UploadVideo(video_repository, mock_storage)

        video_id = uuid4()

        with pytest.raises(VideoNotFound, match='Video with id .* not found') as exc_info:
            use_case.execute(
                UploadVideo.Input(
                    video_id=video_id,
                    file_name='trailer.mp4',
                    content=b'video content',
                    content_type='video/mp4'
                )
            )