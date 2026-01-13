from uuid import uuid4

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.exceptions import RelatedCategoriesNotFound
from src.core.genre.application.usecase.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def series_category() -> Category:
    return Category(name='Series', description='Category for series')


@pytest.fixture
def films_category() -> Category:
    return Category(name='Films', description='Category for films')


@pytest.fixture
def documentary_category() -> Category:
    return Category(name='Documentary', description='Category for documentaries')


@pytest.fixture
def comedy_genre(series_category: Category, films_category: Category) -> Genre:
    return Genre(name='Comedy', categories={series_category.id, films_category.id})


@pytest.fixture
def drama_genre() -> Genre:
    return Genre(name='Drama', is_active=False)


@pytest.fixture
def genre_repository(comedy_genre: Genre, drama_genre: Genre) -> InMemoryGenreRepository:
    return InMemoryGenreRepository(genres=[comedy_genre, drama_genre])


@pytest.fixture
def category_repository(series_category: Category, films_category: Category,
                        documentary_category: Category) -> InMemoryCategoryRepository:
    return InMemoryCategoryRepository(categories=[series_category, films_category, documentary_category])


class TestUpdateGenre:
    def test_activate_genre(self, drama_genre: Genre, genre_repository: InMemoryGenreRepository,
                            category_repository: InMemoryCategoryRepository):
        use_case = UpdateGenre(genre_repository=genre_repository, category_repository=category_repository)
        request = UpdateGenre.Input(id=drama_genre.id, is_active=True)

        use_case.execute(request)

        genre_updated = genre_repository.get_by_id(drama_genre.id)

        assert genre_updated.is_active is True
        assert genre_updated.name == drama_genre.name
        assert genre_updated.categories == drama_genre.categories

    def test_deactivate_genre(self, comedy_genre: Genre, genre_repository: InMemoryGenreRepository,
                              category_repository: InMemoryCategoryRepository):
        use_case = UpdateGenre(genre_repository=genre_repository, category_repository=category_repository)
        request = UpdateGenre.Input(id=comedy_genre.id, is_active=False)

        use_case.execute(request)

        genre_updated = genre_repository.get_by_id(comedy_genre.id)

        assert genre_updated.is_active is False
        assert genre_updated.name == comedy_genre.name
        assert genre_updated.categories == comedy_genre.categories

    def test_update_genre(self, comedy_genre: Genre, films_category: Category, documentary_category: Category,
                          genre_repository: InMemoryGenreRepository, category_repository: InMemoryCategoryRepository):

        use_case = UpdateGenre(genre_repository=genre_repository, category_repository=category_repository)
        request = UpdateGenre.Input(
            id=comedy_genre.id,
            name='Dark Comedy',
            category_ids={films_category.id, documentary_category.id}
        )

        use_case.execute(request)
        genre_updated = genre_repository.get_by_id(comedy_genre.id)

        assert genre_updated.name == 'Dark Comedy'
        assert genre_updated.categories == {films_category.id, documentary_category.id}
        assert genre_updated.is_active == comedy_genre.is_active

    def test_update_genre_when_categories_are_empty(self, comedy_genre: Genre,
                                         genre_repository: InMemoryGenreRepository,
                                         category_repository: InMemoryCategoryRepository):
        use_case = UpdateGenre(genre_repository=genre_repository, category_repository=category_repository)
        request = UpdateGenre.Input(
            id=comedy_genre.id,
            name='Dark Comedy',
            category_ids=set()
        )

        use_case.execute(request)
        genre_updated = genre_repository.get_by_id(comedy_genre.id)

        assert genre_updated.name == 'Dark Comedy'
        assert genre_updated.categories == set()
        assert genre_updated.is_active == comedy_genre.is_active

    def test_update_genre_when_category_does_not_exist(self, comedy_genre: Genre,
                                              genre_repository: InMemoryGenreRepository,
                                              category_repository: InMemoryCategoryRepository):
        use_case = UpdateGenre(genre_repository=genre_repository, category_repository=category_repository)
        non_existent_category_id = uuid4()
        request = UpdateGenre.Input(
            id=comedy_genre.id,
            name='Dark Comedy',
            category_ids={non_existent_category_id}
        )

        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(request)

        assert str(exc_info.value) == f'Categories not found: { {non_existent_category_id} }'

        genre_updated = genre_repository.get_by_id(comedy_genre.id)

        # Ensure the genre was not updated
        assert genre_updated.name == comedy_genre.name
        assert genre_updated.categories == comedy_genre.categories
        assert genre_updated.is_active == comedy_genre.is_active
