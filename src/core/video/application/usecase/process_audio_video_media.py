from src.core.video.application.exceptions import InvalidMediaType, MediaNotFound, VideoNotFound
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.value_objects import MediaType, MediaStatus
from dataclasses import dataclass
from uuid import UUID

class ProcessAudioVideoMedia:

    @dataclass
    class Input:
        video_id: UUID
        encoded_location: str
        media_type: MediaType
        status: MediaStatus

    def __init__(self, video_repository: VideoRepository):
        self.video_repository = video_repository

    def execute(self, input: Input):
        if input.media_type not in [MediaType.VIDEO, MediaType.TRAILER]:
            raise InvalidMediaType("Invalid media type")
        
        video = self.video_repository.get_by_id(input.video_id)
        if not video:
            raise VideoNotFound(f"Video with ID {input.video_id} not found")

        if input.media_type == MediaType.VIDEO:
            if not video.video:
                raise MediaNotFound("Video must have a video media to be processed")

            video.process_video(input.status, input.encoded_location)
        else:
            if not video.trailer:
                raise MediaNotFound("Video must have a trailer media to be processed")

            video.process_trailer(input.status, input.encoded_location)
        self.video_repository.update(video)