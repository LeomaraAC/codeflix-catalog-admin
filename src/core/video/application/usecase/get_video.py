from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core.video.application.exceptions import VideoNotFound
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video_repository import VideoRepository


class GetVideo:
    def __init__(self, repository: VideoRepository):
        self.video_repository = repository

    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        id: UUID
        title: str
        description: str
        launch_year: int
        duration: Decimal
        published: bool
        rating: Rating
        categories: set[UUID]
        genres: set[UUID]
        cast_members: set[UUID]

    def execute(self, input: Input) -> Output:
        video = self.video_repository.get_by_id(input.id)
        if not video:
            raise VideoNotFound(f'Video with id {input.id} not found')

        return self.Output(
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