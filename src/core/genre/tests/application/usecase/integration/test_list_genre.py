import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.usecase.list_genre import ListGenre, GenreOutput
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def action_genre(movie_category: Category, documentary_category: Category) -> Genre:
    return Genre(name='Action', categories={movie_category.id, documentary_category.id})


@pytest.fixture
def horror_genre() -> Genre:
    return Genre(name='Horror')


@pytest.fixture
def genre_repository_with_data(action_genre: Genre, horror_genre: Genre) -> InMemoryGenreRepository:
    return InMemoryGenreRepository(genres=[action_genre, horror_genre])


class TestListGenre:
    def test_list_genre_with_associated_categories(self, action_genre: Genre, horror_genre: Genre,
                                                   genre_repository_with_data: InMemoryGenreRepository):
        use_case = ListGenre(repository=genre_repository_with_data)
        output = use_case.execute(input=ListGenre.Input())
        assert len(output.data) == 2
        assert GenreOutput(id=action_genre.id, name=action_genre.name, is_active=action_genre.is_active,
                           categories=action_genre.categories) in output.data
        assert GenreOutput(id=horror_genre.id, name=horror_genre.name, is_active=horror_genre.is_active,
                           categories=horror_genre.categories) in output.data

    def test_list_genre_empty_repository(self):
        genre_repository = InMemoryGenreRepository()
        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())
        assert len(output.data) == 0

    def test_list_genre_with_no_associated_categories(self, horror_genre: Genre):
        use_case = ListGenre(repository=InMemoryGenreRepository(genres=[horror_genre]))
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1
        horror_output = next((genre for genre in output.data if genre.id == horror_genre.id), None)

        assert horror_output is not None
        assert horror_output.categories == set()
