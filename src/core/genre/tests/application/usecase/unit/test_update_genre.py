import re
from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.usecase.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


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
def genre_repository():
    return create_autospec(GenreRepository)


@pytest.fixture
def category_repository():
    return create_autospec(CategoryRepository)


class TestUpdateGenre:
    def test_when_genre_does_not_exist_then_return_genre_not_found_exception(self, genre_repository,
                                                                             category_repository):
        genre_repository.get_by_id.return_value = None

        genre_id = uuid4()

        use_case = UpdateGenre(genre_repository=genre_repository, category_repository=category_repository)
        with pytest.raises(GenreNotFound, match='Genre with ID .* not found'):
            use_case.execute(UpdateGenre.Input(id=genre_id))

        genre_repository.get_by_id.assert_called_once_with(id=genre_id)
        genre_repository.update.assert_not_called()

    def test_when_genre_data_is_invalid_then_return_invalid_genre_exception(self, comedy_genre: Genre,
                                                                            series_category: Category,
                                                                            films_category: Category,
                                                                            genre_repository,
                                                                            category_repository):
        genre_repository.get_by_id.return_value = comedy_genre
        category_repository.list.return_value = [series_category, films_category]


        use_case = UpdateGenre(genre_repository=genre_repository, category_repository=category_repository)

        input_data = UpdateGenre.Input(id=comedy_genre.id, name='')
        with pytest.raises(InvalidGenre, match='name cannot be empty'):
            use_case.execute(input_data)

        genre_repository.get_by_id.assert_called_once_with(id=comedy_genre.id)

        input_data.name = 'a' * 256
        with pytest.raises(InvalidGenre, match='name cannot be longer than 255 characters'):
            use_case.execute(input_data)

        genre_repository.update.assert_not_called()

    def test_when_genre_categories_do_not_exist_then_return_related_categories_not_found_exception(self,
                                                                                                   comedy_genre: Genre,
                                                                                                   genre_repository,
                                                                                                   category_repository):
        genre_repository.get_by_id.return_value = comedy_genre
        category_repository.list.return_value = []

        use_case = UpdateGenre(genre_repository=genre_repository, category_repository=category_repository)

        category_ids = {uuid4()}

        input_data = UpdateGenre.Input(id=comedy_genre.id, category_ids=category_ids)
        with pytest.raises(RelatedCategoriesNotFound, match=re.escape(f'Categories not found: {category_ids}')):
            use_case.execute(input_data)

        genre_repository.update.assert_not_called()
        category_repository.list.assert_called_once()

    def test_when_genre_and_categories_exist_then_return_success(self, comedy_genre: Genre,
                                                                 documentary_category: Category,
                                                                 films_category: Category, series_category: Category,
                                                                 genre_repository, category_repository):
        genre_repository.get_by_id.return_value = comedy_genre
        category_repository.list.return_value = [documentary_category, films_category, series_category]

        use_case = UpdateGenre(genre_repository=genre_repository, category_repository=category_repository)
        input_data = UpdateGenre.Input(id=comedy_genre.id, name='Comedy!', is_active=False,
                                       category_ids={documentary_category.id, films_category.id})

        use_case.execute(input_data)

        genre_repository.get_by_id.assert_called_once_with(id=comedy_genre.id)
        category_repository.list.assert_called_once()
        genre_repository.update.assert_called_once()
