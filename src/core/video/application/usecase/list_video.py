from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.application.list_response import ListResponse, ListOutputMeta
from src.core._shared.application.list_utils import ListUtils
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video_repository import VideoRepository


class ListVideo:
    def __init__(self, repository: VideoRepository):
        self.video_repository = repository

    @dataclass
    class Input:
        order_by: str = 'title'
        current_page: int = 1

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

    def execute(self, input: Input) -> ListResponse[Output]:
        videos = self.video_repository.list()
        sorted_videos = ListUtils.sort(
            [
                self.Output(
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
                for video in videos
            ],
            input.order_by,
        )
        videos_page = ListUtils.paginate(sorted_videos, input.current_page)

        return ListResponse[self.Output](
            data=videos_page,
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=ListUtils.DEFAULT_PAGE_SIZE,
                total=len(sorted_videos),
            ),
        )