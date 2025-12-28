import uuid

from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestSave:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(name='Series', description='Category for series')

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

class TestGetById:
    def test_can_get_category_by_id(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series', is_active=False)
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])

        response = repository.get_by_id(id = category_series.id)

        assert response is not None
        assert response == category_series

    def test_when_category_does_not_exist_then_return_none(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series', is_active=False)
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])
        not_found_id = uuid.uuid4()

        response = repository.get_by_id(id = not_found_id)

        assert response is None