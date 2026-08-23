from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from src.core._shared.infrastructure.storage.local_storage import LocalStorage
from src.core.video.domain.value_objects import MediaStatus
from src.django_project.video_app import views as video_views
from src.django_project.video_app.models import AudioVideoMedia, Video


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def local_storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> LocalStorage:
    storage = LocalStorage(bucket=str(tmp_path))
    monkeypatch.setattr(video_views, 'LocalStorage', lambda: storage)
    return storage


@pytest.mark.django_db
class TestUploadVideo:
    def test_user_can_upload_video_file(self, api_client: APIClient, local_storage: LocalStorage,) -> None:
        category_response = api_client.post(
            '/api/categories/',
            {
                'name': 'Movie',
                'description': 'Movie category',
            },
            format='json',
        )
        genre_response = api_client.post(
            '/api/genres/',
            {
                'name': 'Action',
                'category_ids': [category_response.data['id']],
            },
            format='json',
        )
        cast_member_response = api_client.post(
            '/api/cast_members/',
            {
                'name': 'Keanu Reeves',
                'type': 'ACTOR',
            },
            format='json',
        )
        create_video_response = api_client.post(
            '/api/videos/',
            {
                'title': 'John Wick',
                'description': 'Action movie',
                'launch_year': 2014,
                'duration': '120.50',
                'rating': 'AGE_16',
                'categories': [category_response.data['id']],
                'genres': [genre_response.data['id']],
                'cast_members': [cast_member_response.data['id']],
            },
            format='json',
        )
        video_id = create_video_response.data['id']
        file_name = 'john-wick.mp4'
        file_content = b'john wick video content'
        video_file = SimpleUploadedFile(
            name=file_name,
            content=file_content,
            content_type='video/mp4',
        )

        upload_response = api_client.patch(
            f'/api/videos/{video_id}/',
            data={'video_file': video_file},
            format='multipart',
        )

        assert upload_response.status_code == 200

        persisted_video = Video.objects.select_related('video').get(id=video_id)
        persisted_media = persisted_video.video
        expected_raw_location = f'videos/{video_id}/{file_name}'

        assert persisted_media is not None
        assert AudioVideoMedia.objects.count() == 1
        assert persisted_media.name == file_name
        assert persisted_media.raw_location == expected_raw_location
        assert persisted_media.encoded_location == ''
        assert persisted_media.status == MediaStatus.PENDING.name

        uploaded_file_path = local_storage.bucket / expected_raw_location

        assert uploaded_file_path.is_file()
        assert uploaded_file_path.read_bytes() == file_content
