from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.domain.notification import Notification
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


class CreateVideoWithoutMedia:
    @dataclass
    class Input:
        title: str
        description: str
        launch_year: int
        duration: Decimal
        rating: str
        categories: set[UUID]
        genres: set[UUID]
        cast_members: set[UUID]
    
    @dataclass
    class Output:
        id: UUID
    
    def __init__(self, video_repository: VideoRepository, category_repository: CategoryRepository, genre_repository: GenreRepository, cast_member_repository: CastMemberRepository):
        self.video_repository = video_repository
        self.category_repository = category_repository
        self.genre_repository = genre_repository
        self.cast_member_repository = cast_member_repository
        self._notification = Notification()
    
    def execute(self, input: Input) -> Output:

        self._validate_categories(input.categories)
        self._validate_genres(input.genres)
        self._validate_cast_members(input.cast_members)

        if self._notification.has_errors:
            raise RelatedEntitiesNotFound(self._notification.messages)

        try:
            video = Video(
                title=input.title,
                description=input.description,
                launch_year=input.launch_year,
                duration=input.duration,
                published=False,
                rating=input.rating,
                categories=input.categories,
                genres=input.genres,
                cast_members=input.cast_members
            )
        except ValueError as e:
            raise InvalidVideo(e)
        
        self.video_repository.save(video)

        return self.Output(id=video.id)
    
    def _validate_categories(self, categories: set[UUID]) -> None:
        category_ids = {category.id for category in self.category_repository.list()}
        if not categories.issubset(category_ids):
            self._notification.add_error('Categories with provided IDs not found')
    
    def _validate_genres(self, genres: set[UUID]) -> None:
        genre_ids = {genre.id for genre in self.genre_repository.list()}
        if not genres.issubset(genre_ids):
            self._notification.add_error('Genres with provided IDs not found')
    
    def _validate_cast_members(self, cast_members: set[UUID]) -> None:
        cast_member_ids = {cast_member.id for cast_member in self.cast_member_repository.list()}
        if not cast_members.issubset(cast_member_ids):
            self._notification.add_error('Cast members with provided IDs not found')
    
