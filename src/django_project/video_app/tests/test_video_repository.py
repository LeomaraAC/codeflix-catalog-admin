from decimal import Decimal

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.models import Video as VideoORM
from src.django_project.video_app.repository import DjangoORMVideoRepository


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestSave:
    def test_can_save_video_with_related_entities(
        self,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        category = Category(name='Movies')
        category_repository.save(category)

        genre = Genre(name='Action', categories={category.id})
        genre_repository.save(genre)

        cast_member = CastMember(name='Keanu Reeves', type=CastMemberType.ACTOR)
        cast_member_repository.save(cast_member)

        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
            published=False,
            rating=Rating.AGE_16,
            categories={category.id},
            genres={genre.id},
            cast_members={cast_member.id},
        )

        repository = DjangoORMVideoRepository()

        repository.save(video)

        saved_video = VideoORM.objects.get(id=video.id)

        assert saved_video.title == video.title
        assert saved_video.description == video.description
        assert saved_video.launch_year == video.launch_year
        assert saved_video.duration == video.duration
        assert saved_video.published == video.published
        assert saved_video.rating == Rating.AGE_16.name
        assert {item.id for item in saved_video.categories.all()} == {category.id}
        assert {item.id for item in saved_video.genres.all()} == {genre.id}
        assert {item.id for item in saved_video.cast_members.all()} == {cast_member.id}


@pytest.mark.django_db
class TestGetById:
    def test_can_rebuild_domain_video_from_database(
        self,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        category = Category(name='Movies')
        category_repository.save(category)

        genre = Genre(name='Action', categories={category.id})
        genre_repository.save(genre)

        cast_member = CastMember(name='Keanu Reeves', type=CastMemberType.ACTOR)
        cast_member_repository.save(cast_member)

        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
            published=False,
            rating=Rating.AGE_16,
            categories={category.id},
            genres={genre.id},
            cast_members={cast_member.id},
        )
        DjangoORMVideoRepository().save(video)

        persisted_video = DjangoORMVideoRepository().get_by_id(video.id)

        assert persisted_video is not None
        assert persisted_video.id == video.id
        assert persisted_video.title == video.title
        assert persisted_video.description == video.description
        assert persisted_video.launch_year == video.launch_year
        assert persisted_video.duration == video.duration
        assert persisted_video.published == video.published
        assert persisted_video.rating == Rating.AGE_16
        assert persisted_video.categories == {category.id}
        assert persisted_video.genres == {genre.id}
        assert persisted_video.cast_members == {cast_member.id}
