from unittest.mock import create_autospec

import pytest

from src.core._shared.infrastructure.abstract_storage_service import AbstractStorageService
from src.core.video.application.exceptions import VideoNotFound
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.application.usecase.upload_video import UploadVideo


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

        mock_repository = create_autospec(VideoRepository)
        mock_repository.get_by_id.return_value = video
        mock_storage = create_autospec(AbstractStorageService)

        use_case = UploadVideo(mock_repository, mock_storage)
        input_data = UploadVideo.Input(
            video_id=video.id,
            file_name='trailer.mp4',
            content=b'video content',
            content_type='video/mp4'
        )

        use_case.execute(input_data)

        mock_repository.get_by_id.assert_called_once_with(video.id)
        mock_storage.store.assert_called_once_with(
            file_path=f'videos/{video.id}/trailer.mp4',
            content=b'video content',
            content_type='video/mp4'
        )
        mock_repository.update.assert_called_once_with(video)
        assert video.video == AudioVideoMedia(
            name='trailer.mp4',
            raw_location=f'videos/{video.id}/trailer.mp4',
            encoded_location='',
            status=MediaStatus.PENDING
        )


    def test_when_video_does_not_exist_should_raise_exception(self):
        mock_repository = create_autospec(VideoRepository)
        mock_repository.get_by_id.return_value = None
        mock_storage = create_autospec(AbstractStorageService)

        use_case = UploadVideo(mock_repository, mock_storage)

        with pytest.raises(VideoNotFound, match=f'Video with id .* not found'):
            use_case.execute(
                UploadVideo.Input(
                    video_id='00000000-0000-0000-0000-000000000000',
                    file_name='trailer.mp4',
                    content=b'video content',
                    content_type='video/mp4'
                )
            )