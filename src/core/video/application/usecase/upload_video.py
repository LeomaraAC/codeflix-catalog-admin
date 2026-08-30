from uuid import UUID
from dataclasses import dataclass
from pathlib import Path
from src.core._shared.events.message_bus import AbstractMessageBus
from src.core.video.domain.value_objects import MediaType
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core._shared.infrastructure.storage.abstract_storage_service import AbstractStorageService
from src.core.video.application.exceptions import VideoNotFound
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus
from src.core.video.domain.video_repository import VideoRepository


class UploadVideo:
    @dataclass
    class Input:
        video_id: UUID
        file_name: str
        content: bytes
        content_type: str


    def __init__(self, video_repository: VideoRepository, storage_service: AbstractStorageService, message_bus: AbstractMessageBus):
        self.video_repository = video_repository
        self.storage_service = storage_service
        self.message_bus = message_bus

    def execute(self, input: Input):
        video = self.video_repository.get_by_id(input.video_id)
        if not video:
            raise VideoNotFound(f'Video with id {input.video_id} not found')

        file_path =  Path('videos') / str(input.video_id) / input.file_name

        self.storage_service.store(
            file_path=str(file_path),
            content=input.content,
            content_type=input.content_type
        )

        audio_video_media = AudioVideoMedia(
            name=input.file_name,
            raw_location=str(file_path),
            encoded_location="",
            status=MediaStatus.PENDING
        )

        video.update_video(audio_video_media)
        self.video_repository.update(video)
        self.message_bus.handle([
            AudioVideoMediaUpdatedIntegrationEvent(
                resource_id=f'{video.id}.{MediaType.VIDEO}',
                file_path=str(file_path)
            )
        ])
