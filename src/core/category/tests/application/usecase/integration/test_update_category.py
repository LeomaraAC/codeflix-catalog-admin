import uuid

import pytest

from src.core.category.application.usecase.exceptions import CategoryNotFound, InvalidCategoryData
from src.core.category.application.usecase.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.application.usecase.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestUpdateCategory:
    def test_update_category_name(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series', is_active=False)
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(id=category_film.id, name='Documentaries')

        use_case.execute(request)

        category_updated = repository.get_by_id(category_film.id)

        assert category_updated.name == 'Documentaries'
        assert category_updated.description == category_film.description
        assert category_updated.is_active == category_film.is_active

    def test_update_category_description(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series', is_active=False)
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(id=category_series.id, description='Category for TV series')

        use_case.execute(request)

        category_updated = repository.get_by_id(category_series.id)

        assert category_updated.name == category_series.name
        assert category_updated.description == 'Category for TV series'
        assert category_updated.is_active == category_series.is_active

    def test_update_category_name_and_description(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series', is_active=False)
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(id=category_series.id, description='Category for TV series', name='TV Series')

        use_case.execute(request)

        category_updated = repository.get_by_id(category_series.id)

        assert category_updated.name == 'TV Series'
        assert category_updated.description == 'Category for TV series'
        assert category_updated.is_active == category_series.is_active

    def test_can_deactivate_category(self):
        category_film = Category(name='Films', description='Category for films', is_active=True)
        repository = InMemoryCategoryRepository(categories=[category_film])

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(id=category_film.id, is_active=False)

        use_case.execute(request)

        category_updated = repository.get_by_id(category_film.id)

        assert category_updated.is_active is False
        assert category_updated.name == category_film.name
        assert category_updated.description == category_film.description

    def test_can_activate_category(self):
        category_film = Category(name='Films', description='Category for films', is_active=False)
        repository = InMemoryCategoryRepository(categories=[category_film])

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(id=category_film.id, is_active=True)

        use_case.execute(request)

        category_updated = repository.get_by_id(category_film.id)

        assert category_updated.is_active is True
        assert category_updated.name == category_film.name
        assert category_updated.description == category_film.description

    def test_when_name_is_invalid_then_raise_exception(self):
        category_film = Category(name='Films', description='Category for films')
        repository = InMemoryCategoryRepository(categories=[category_film])

        use_case = UpdateCategory(repository=repository)
        with pytest.raises(InvalidCategoryData):
            use_case.execute(request=UpdateCategoryRequest(id=category_film.id, name='a'*256))

        category_found = repository.get_by_id(category_film.id)
        assert len(repository.categories) == 1
        assert category_found == category_film
        assert category_found.description == category_film.description
        assert category_found.name == category_film.name
        assert category_found.is_active == category_film.is_active

    def test_when_category_does_not_exist_then_raise_exception(self):
        category_film = Category(name='Films', description='Category for films')
        repository = InMemoryCategoryRepository(categories=[category_film])

        use_case = UpdateCategory(repository=repository)
        with pytest.raises(CategoryNotFound):
            use_case.execute(request=UpdateCategoryRequest(id=uuid.uuid4(), name='Nonexistent Category'))

        category_found = repository.get_by_id(category_film.id)
        assert len(repository.categories) == 1
        assert category_found == category_film
        assert category_found.description == category_film.description
        assert category_found.name == category_film.name
        assert category_found.is_active == category_film.is_active