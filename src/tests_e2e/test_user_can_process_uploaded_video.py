from pathlib import Path

import pika
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from rest_framework.test import APIClient

from src.core._shared.infrastructure.storage.local_storage import LocalStorage
from src.core.video.domain.value_objects import MediaStatus
from src.django_project.video_app import views as video_views
from src.django_project.video_app.models import Video


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def local_storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> LocalStorage:
    storage = LocalStorage(bucket=str(tmp_path))
    monkeypatch.setattr(video_views, 'LocalStorage', lambda: storage)
    return storage


@pytest.fixture
def bounded_consumer(monkeypatch: pytest.MonkeyPatch) -> None:
    start_consuming = pika.adapters.blocking_connection.BlockingChannel.start_consuming

    def start_consuming_with_timeout(channel):
        connection = channel.connection
        timer = connection.call_later(1, channel.stop_consuming)
        try:
            return start_consuming(channel)
        finally:
            if connection.is_open:
                connection.remove_timeout(timer)
                connection.close()
                
    monkeypatch.setattr(
        pika.adapters.blocking_connection.BlockingChannel,
        'start_consuming',
        start_consuming_with_timeout,
    )


@pytest.mark.django_db
class TestCompleteVideoProcessing:
    @pytest.mark.usefixtures('bounded_consumer')
    def test_user_can_process_uploaded_video_after_receiving_converted_event(self, api_client: APIClient, local_storage: LocalStorage,) -> None:
        category_response = api_client.post(
            '/api/categories/',
            {'name': 'Movie', 'description': 'Movie category'},
            format='json',
        )
        assert category_response.status_code == 201

        genre_response = api_client.post(
            '/api/genres/',
            {'name': 'Action', 'category_ids': [category_response.data['id']]},
            format='json',
        )
        assert genre_response.status_code == 201

        cast_member_response = api_client.post(
            '/api/cast_members/',
            {'name': 'Keanu Reeves', 'type': 'ACTOR'},
            format='json',
        )
        assert cast_member_response.status_code == 201

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
        assert create_video_response.status_code == 201
        video_id = create_video_response.data['id']

        file_name = 'john-wick.mp4'
        file_content = b'john wick video content'
        upload_response = api_client.patch(
            f'/api/videos/{video_id}/',
            data={
                'video_file': SimpleUploadedFile(name=file_name, content=file_content, content_type='video/mp4'),
            },
            format='multipart',
        )
        assert upload_response.status_code == 200

        persisted_video = Video.objects.select_related('video').get(id=video_id)
        assert persisted_video.video is not None
        assert persisted_video.video.status == MediaStatus.PENDING.name
        assert persisted_video.video.encoded_location == ''
        expected_raw_location = f'videos/{video_id}/{file_name}'
        assert (local_storage.bucket / expected_raw_location).read_bytes() == file_content

        send_message_to_rabbitmq(video_id=video_id)
        call_command('start_consumer')
        persisted_video = Video.objects.select_related('video').get(id=video_id)
        assert persisted_video.video.status == MediaStatus.COMPLETED.name, (
            'Video was not processed within 1 second after the converted event'
        )
        assert persisted_video.video.encoded_location == '/path/to/encoded/video'
        assert persisted_video.video.raw_location == expected_raw_location
        assert persisted_video.video.name == file_name


def send_message_to_rabbitmq(video_id: str, queue: str = "videos.converted", host: str = "localhost", port: int = 5672):
    import json
    import pika

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=port,
        ),
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    message = {
        "error": "",
        "video": {
            "resource_id": f"{video_id}.VIDEO",
            "encoded_video_folder": "/path/to/encoded/video",
        },
        "status": "COMPLETED",
    }
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message))

    print("Sent message")
    connection.close()
