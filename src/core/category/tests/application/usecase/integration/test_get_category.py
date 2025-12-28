import uuid

import pytest

from src.core.category.application.usecase.exceptions import CategoryNotFound
from src.core.category.application.usecase.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestGetCategory:
    def test_get_category_by_id(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series', is_active=False)
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])

        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(id=category_film.id)

        response = use_case.execute(request)

        assert response == GetCategoryResponse(id=category_film.id, name=category_film.name,
                                               description=category_film.description, is_active=category_film.is_active)

    def test_when_category_does_not_exist_then_raise_exception(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series', is_active=False)
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])

        use_case = GetCategory(repository=repository)
        with pytest.raises(CategoryNotFound):
            use_case.execute(request=GetCategoryRequest(id=uuid.uuid4()))