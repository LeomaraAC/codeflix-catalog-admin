import uuid

import pytest

from src.core.category.application.usecase.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.usecase.exceptions import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestDeleteCategory:
    def test_get_category_by_id(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series')
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])

        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(id=category_film.id)

        assert repository.get_by_id(category_film.id) is not None
        assert repository.get_by_id(category_series.id) is not None
        use_case.execute(request)

        assert repository.get_by_id(category_film.id) is None
        assert repository.get_by_id(category_series.id) is not None

    def test_when_category_does_not_exist_then_raise_exception(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series', is_active=False)
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])

        use_case = DeleteCategory(repository=repository)
        with pytest.raises(CategoryNotFound):
            use_case.execute(request=DeleteCategoryRequest(id=uuid.uuid4()))

        assert len(repository.categories) == 2
        assert repository.get_by_id(category_film.id) is not None
        assert repository.get_by_id(category_series.id) is not None