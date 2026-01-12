import re
from unittest.mock import create_autospec
from uuid import uuid4, UUID

import pytest

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.application.exceptions import RelatedCategoriesNotFound
from src.core.genre.application.usecase.create_genre import CreateGenre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


class TestCreateGenre:
    def test_create_genre_with_associated_categories(self, movie_category: Category, documentary_category: Category):
        category_repository = InMemoryCategoryRepository(categories=[movie_category, documentary_category])
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=category_repository,
        )

        input = CreateGenre.Input(
            name='Action',
            category_ids={movie_category.id, documentary_category.id}
        )

        output = use_case.execute(input=input)

        saved_genre = genre_repository.get_by_id(output.id)

        assert output.id is not None
        assert isinstance(output.id, UUID)
        assert saved_genre.name == input.name
        assert saved_genre.categories == input.category_ids
        assert saved_genre.is_active is True


    def test_create_genre_with_inexistent_categories_raise_exception(self):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=InMemoryCategoryRepository(),
        )
        category_id = {uuid4()}

        with pytest.raises(RelatedCategoriesNotFound, match=re.escape(rf'Categories not found: {category_id}')):
            use_case.execute(input=CreateGenre.Input(name='Action', category_ids=category_id))

        assert len(genre_repository.list()) == 0


    def test_create_genre_without_categories(self):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository=InMemoryCategoryRepository(),
        )

        input = CreateGenre.Input(name='Horror')

        output = use_case.execute(input=input)

        saved_genre = genre_repository.get_by_id(output.id)

        assert output.id is not None
        assert isinstance(output.id, UUID)
        assert saved_genre.name == input.name
        assert saved_genre.categories == set()
        assert saved_genre.is_active is True
        assert len(genre_repository.list()) == 1
