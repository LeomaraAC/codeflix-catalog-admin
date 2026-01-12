from os import name
from unittest.mock import create_autospec
from uuid import uuid4, UUID

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import RelatedCategoriesNotFound, InvalidGenre
from src.core.genre.application.usecase.create_genre import CreateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def mock_category_repository_with_categories(movie_category, documentary_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository


class TestCreateGenre:
    def test_when_categories_do_not_exist_should_raise_related_categories_not_found(
            self,
            mock_genre_repository: GenreRepository,
            mock_empty_category_repository: CategoryRepository,
    ):
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_empty_category_repository,
        )
        category_id = uuid4()

        with pytest.raises(RelatedCategoriesNotFound) as exec_info:
            use_case.execute(input=CreateGenre.Input(name='Action', category_ids={category_id}))

        assert str(category_id) in str(exec_info.value)

    def test_when_created_genre_is_invalid_then_raise_invalid_genre(self,
                                                                    movie_category: Category,
                                                                    mock_genre_repository: GenreRepository,
                                                                    mock_category_repository_with_categories: CategoryRepository
                                                                    ):
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )

        input = CreateGenre.Input(
            name='',
            category_ids={movie_category.id}
        )

        with pytest.raises(InvalidGenre, match='name cannot be empty'):
            use_case.execute(input=input)

    def test_when_created_genre_is_valid_and_categories_exist_then_save_genre(self,
                                                                              movie_category: Category,
                                                                              documentary_category: Category,
                                                                              mock_genre_repository: GenreRepository,
                                                                              mock_category_repository_with_categories: CategoryRepository
                                                                              ):
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )

        input = CreateGenre.Input(
            name='Action',
            category_ids={movie_category.id, documentary_category.id}
        )


        output = use_case.execute(input=input)

        assert output.id is not None
        assert isinstance(output.id, UUID)
        mock_genre_repository.save.assert_called_once_with(
            Genre(name=input.name, categories=input.category_ids, is_active=True, id=output.id)
        )

    def test_create_genre_without_categories(self,
                                              mock_genre_repository: GenreRepository,
                                              mock_category_repository_with_categories: CategoryRepository
                                              ):
        use_case = CreateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )

        input = CreateGenre.Input(
            name='Horror',
            category_ids=set()
        )

        output = use_case.execute(input=input)

        assert output.id is not None
        assert isinstance(output.id, UUID)
        mock_genre_repository.save.assert_called_once_with(
            Genre(name=input.name, categories=input.category_ids, is_active=True, id=output.id)
        )
