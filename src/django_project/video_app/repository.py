from django.db import transaction
from uuid import UUID

from src.core.video.domain.video import Video
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video_repository import VideoRepository
from .models import Video as VideoORM


class DjangoORMVideoRepository(VideoRepository):
    def save(self, video: Video) -> None:
        with transaction.atomic():
            video_model = VideoModelMapper.to_model_orm(video)
            video_model.save()
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)
    
    def get_by_id(self, id: UUID) -> Video | None:
        try:
            video_orm = VideoORM.objects.get(id=id)
        except VideoORM.DoesNotExist:
            return None
        return VideoModelMapper.to_entity(video_orm)
    
    def delete(self, id: UUID) -> None:
        VideoORM.objects.filter(id=id).delete()

    def update(self, video: Video) -> None:
        pass  # Implement the update method if needed

    def list(self) -> list[Video]:
        return [
            VideoModelMapper.to_entity(video_model)
            for video_model in VideoORM.objects.all()
        ]

class VideoModelMapper:
    @staticmethod
    def to_entity(video: VideoORM) -> Video:
        return Video(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            published=video.published,
            rating=Rating[video.rating],
            categories={cat.id for cat in video.categories.all()},
            genres={gen.id for gen in video.genres.all()},
            cast_members={cast.id for cast in video.cast_members.all()},
        )

    @staticmethod
    def to_model_orm(video: Video) -> VideoORM:
        return VideoORM(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            published=video.published,
            rating=video.rating.name,
            duration=video.duration,
        )