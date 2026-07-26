from decimal import Decimal
from unittest.mock import create_autospec
from uuid import UUID, uuid4

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.application.usecase.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video_repository import VideoRepository


@pytest.fixture
def mock_video_repository() -> VideoRepository:
    return create_autospec(VideoRepository)


@pytest.fixture
def movie_category() -> Category:
    return Category(name='Movies')


@pytest.fixture
def action_genre() -> Genre:
    return Genre(name='Action')


@pytest.fixture
def cast_member() -> CastMember:
    return CastMember(name='Keanu Reeves', type=CastMemberType.ACTOR)


@pytest.fixture
def mock_category_repository_with_data(movie_category: Category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category]
    return repository


@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository


@pytest.fixture
def mock_genre_repository_with_data(action_genre: Genre) -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.list.return_value = [action_genre]
    return repository


@pytest.fixture
def mock_empty_genre_repository() -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.list.return_value = []
    return repository


@pytest.fixture
def mock_cast_member_repository_with_data(cast_member: CastMember) -> CastMemberRepository:
    repository = create_autospec(CastMemberRepository)
    repository.list.return_value = [cast_member]
    return repository


@pytest.fixture
def mock_empty_cast_member_repository() -> CastMemberRepository:
    repository = create_autospec(CastMemberRepository)
    repository.list.return_value = []
    return repository

DEFAULT_VIDEO = {
	'title': 'John Wick',
	'description': 'An action movie',
	'launch_year': 2014,
	'duration': Decimal('101'),
	'rating': Rating.AGE_16,
}
    
class TestCreateVideoWithoutMedia:
    
    def test_create_video_with_valid_data(
        self,
        mock_video_repository: VideoRepository,
        mock_category_repository_with_data: CategoryRepository,
        mock_genre_repository_with_data: GenreRepository,
        mock_cast_member_repository_with_data: CastMemberRepository,
        movie_category: Category,
        action_genre: Genre,
        cast_member: CastMember,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository_with_data,
            genre_repository=mock_genre_repository_with_data,
            cast_member_repository=mock_cast_member_repository_with_data,
        )

        response = use_case.execute(
            self._build_input(
                categories={movie_category.id},
                genres={action_genre.id},
                cast_members={cast_member.id},
            )
        )

        persisted_video = mock_video_repository.save.call_args.args[0]

        assert response is not None
        assert isinstance(response.id, UUID)
        assert persisted_video.id == response.id
        assert persisted_video.title == DEFAULT_VIDEO['title']
        assert persisted_video.description == DEFAULT_VIDEO['description']
        assert persisted_video.launch_year == DEFAULT_VIDEO['launch_year']
        assert persisted_video.duration == DEFAULT_VIDEO['duration']
        assert persisted_video.rating == DEFAULT_VIDEO['rating']
        assert persisted_video.published is False
        assert persisted_video.categories == {movie_category.id}
        assert persisted_video.genres == {action_genre.id}
        assert persisted_video.cast_members == {cast_member.id}
        mock_video_repository.save.assert_called_once()

    def test_raise_exception_when_categories_and_cast_members_are_invalid(
        self,
        mock_video_repository: VideoRepository,
        mock_empty_category_repository: CategoryRepository,
        mock_genre_repository_with_data: GenreRepository,
        mock_empty_cast_member_repository: CastMemberRepository,
        action_genre: Genre,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_empty_category_repository,
            genre_repository=mock_genre_repository_with_data,
            cast_member_repository=mock_empty_cast_member_repository,
        )

        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(
                self._build_input(
                    categories={uuid4()},
                    genres={action_genre.id},
                    cast_members={uuid4()},
                )
            )

        assert 'Categories with provided IDs not found' in str(exc_info.value)
        assert 'Cast members with provided IDs not found' in str(exc_info.value)
        mock_video_repository.save.assert_not_called()

    def test_raise_exception_when_genres_are_invalid(
        self,
        mock_video_repository: VideoRepository,
        mock_category_repository_with_data: CategoryRepository,
        mock_empty_genre_repository: GenreRepository,
        mock_cast_member_repository_with_data: CastMemberRepository,
        movie_category: Category,
        cast_member: CastMember,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository_with_data,
            genre_repository=mock_empty_genre_repository,
            cast_member_repository=mock_cast_member_repository_with_data,
        )

        with pytest.raises(RelatedEntitiesNotFound, match='Genres with provided IDs not found'):
            use_case.execute(
                self._build_input(
                    categories={movie_category.id},
                    genres={uuid4()},
                    cast_members={cast_member.id},
                )
            )

        mock_video_repository.save.assert_not_called()

    def test_raise_exception_when_video_data_is_invalid(
        self,
        mock_video_repository: VideoRepository,
        mock_category_repository_with_data: CategoryRepository,
        mock_genre_repository_with_data: GenreRepository,
        mock_cast_member_repository_with_data: CastMemberRepository,
        movie_category: Category,
        action_genre: Genre,
        cast_member: CastMember,
    ):
        use_case = CreateVideoWithoutMedia(
            video_repository=mock_video_repository,
            category_repository=mock_category_repository_with_data,
            genre_repository=mock_genre_repository_with_data,
            cast_member_repository=mock_cast_member_repository_with_data,
        )

        with pytest.raises(InvalidVideo) as exc_info:
            use_case.execute(
                self._build_input(
                    title='',
                    categories={movie_category.id},
                    genres={action_genre.id},
                    cast_members={cast_member.id},
                )
            )

        assert 'Title cannot be empty' in str(exc_info.value)
        mock_video_repository.save.assert_not_called()

    @staticmethod
    def _build_input(
        title: str = DEFAULT_VIDEO['title'],
        description: str = DEFAULT_VIDEO['description'],
        launch_year: int = DEFAULT_VIDEO['launch_year'],
        duration: Decimal = DEFAULT_VIDEO['duration'],
        rating: Rating = DEFAULT_VIDEO['rating'],
        categories: set[UUID] | None = None,
        genres: set[UUID] | None = None,
        cast_members: set[UUID] | None = None,
    ) -> CreateVideoWithoutMedia.Input:
        return CreateVideoWithoutMedia.Input(
            title=title,
            description=description,
            launch_year=launch_year,
            duration=duration,
            rating=rating,
            categories=categories or set(),
            genres=genres or set(),
            cast_members=cast_members or set(),
        )
