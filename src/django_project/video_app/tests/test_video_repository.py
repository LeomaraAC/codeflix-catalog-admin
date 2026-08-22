from decimal import Decimal
from uuid import uuid4

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, Rating
from src.core.video.domain.video import Video
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.models import AudioVideoMedia as AudioVideoMediaORM
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


@pytest.mark.django_db
class TestUpdate:
    def test_can_update_video_in_database(
        self,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        category_movies = Category(name='Movies')
        category_series = Category(name='Series')
        category_repository.save(category_movies)
        category_repository.save(category_series)

        genre_action = Genre(name='Action', categories={category_movies.id})
        genre_drama = Genre(name='Drama', categories={category_series.id})
        genre_repository.save(genre_action)
        genre_repository.save(genre_drama)

        cast_member_actor = CastMember(name='Keanu Reeves', type=CastMemberType.ACTOR)
        cast_member_director = CastMember(name='Chad Stahelski', type=CastMemberType.DIRECTOR)
        cast_member_repository.save(cast_member_actor)
        cast_member_repository.save(cast_member_director)

        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
            published=False,
            rating=Rating.AGE_16,
            categories={category_movies.id},
            genres={genre_action.id},
            cast_members={cast_member_actor.id},
        )
        repository = DjangoORMVideoRepository()
        repository.save(video)

        video_to_update = Video(
            id=video.id,
            title='John Wick: Chapter 4',
            description='Updated action movie',
            launch_year=2023,
            duration=Decimal('169.00'),
            published=True,
            rating=Rating.AGE_18,
            categories={category_series.id},
            genres={genre_drama.id},
            cast_members={cast_member_director.id},
            video=AudioVideoMedia(
                name='john-wick-4.mp4',
                raw_location='videos/john-wick-4.mp4',
                encoded_location='videos/john-wick-4-encoded.mp4',
                status=MediaStatus.COMPLETED,
            ),
        )

        repository.update(video_to_update)

        updated_video = VideoORM.objects.get(id=video.id)

        assert updated_video.title == video_to_update.title
        assert updated_video.description == video_to_update.description
        assert updated_video.launch_year == video_to_update.launch_year
        assert updated_video.duration == video_to_update.duration
        assert updated_video.published == video_to_update.published
        assert updated_video.rating == video_to_update.rating.name
        assert {item.id for item in updated_video.categories.all()} == {category_series.id}
        assert {item.id for item in updated_video.genres.all()} == {genre_drama.id}
        assert {item.id for item in updated_video.cast_members.all()} == {cast_member_director.id}
        assert updated_video.video is not None
        assert updated_video.video.name == video_to_update.video.name
        assert updated_video.video.raw_location == video_to_update.video.raw_location
        assert updated_video.video.encoded_location == video_to_update.video.encoded_location
        assert updated_video.video.status == video_to_update.video.status.name

    def test_when_updating_video_media_then_previous_media_is_deleted(self) -> None:
        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
            published=False,
            rating=Rating.AGE_16,
            categories=set(),
            genres=set(),
            cast_members=set(),
            video=AudioVideoMedia(
                name='john-wick.mp4',
                raw_location='videos/john-wick.mp4',
                encoded_location='',
                status=MediaStatus.PENDING,
            ),
        )
        repository = DjangoORMVideoRepository()
        repository.save(video)

        persisted_video = VideoORM.objects.get(id=video.id)
        previous_media_id = persisted_video.video_id

        video.update_video(
            AudioVideoMedia(
                name='john-wick-new.mp4',
                raw_location='videos/john-wick-new.mp4',
                encoded_location='',
                status=MediaStatus.PENDING,
            )
        )
        repository.update(video)

        updated_video = VideoORM.objects.get(id=video.id)

        assert AudioVideoMediaORM.objects.filter(id=previous_media_id).count() == 0
        assert AudioVideoMediaORM.objects.count() == 1
        assert updated_video.video.name == 'john-wick-new.mp4'

    def test_when_video_does_not_exist_then_no_effect(self) -> None:
        video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('120.50'),
            published=False,
            rating=Rating.AGE_16,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        repository = DjangoORMVideoRepository()
        repository.save(video)

        nonexistent_video = Video(
            id=uuid4(),
            title='Nonexistent Video',
            description='This video does not exist',
            launch_year=2026,
            duration=Decimal('90.00'),
            published=True,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
            video=AudioVideoMedia(
                name='nonexistent.mp4',
                raw_location='videos/nonexistent.mp4',
                encoded_location='',
                status=MediaStatus.PENDING,
            ),
        )

        repository.update(nonexistent_video)

        existing_video = VideoORM.objects.get(id=video.id)

        assert VideoORM.objects.count() == 1
        assert AudioVideoMediaORM.objects.count() == 0
        assert existing_video.title == video.title
        assert existing_video.description == video.description
        assert existing_video.launch_year == video.launch_year
        assert existing_video.duration == video.duration
        assert existing_video.published == video.published
        assert existing_video.rating == video.rating.name
