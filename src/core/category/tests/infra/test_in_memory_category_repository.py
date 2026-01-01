import copy
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

class TestDelete:
    def test_can_delete_category_by_id(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series')
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])

        repository.delete(id=category_film.id)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category_series

    def test_when_category_does_not_exist_then_no_effect(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series')
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])
        not_found_id = uuid.uuid4()

        repository.delete(id=not_found_id)

        assert len(repository.categories) == 2
        assert repository.categories[0] == category_film
        assert repository.categories[1] == category_series

class TestUpdate:
    def test_can_update_category_name(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series')
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])
        category_to_update = copy.deepcopy(category_film)
        category_to_update.name = 'Documentaries'

        repository.update(category=category_to_update)

        assert len(repository.categories) == 2
        assert repository.categories[0] == category_film
        assert repository.categories[0].name == category_to_update.name
        assert repository.categories[0].is_active == category_film.is_active
        assert repository.categories[0].description == category_film.description

    def test_can_update_category_description(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series')
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])
        category_to_update = copy.deepcopy(category_series)
        category_to_update.description = 'Category for TV series'

        repository.update(category=category_to_update)

        assert len(repository.categories) == 2
        assert repository.categories[1] == category_series
        assert repository.categories[1].name == category_series.name
        assert repository.categories[1].description == category_to_update.description
        assert repository.categories[1].is_active == category_series.is_active

    def test_can_update_category_name_and_description(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series')
        repository = InMemoryCategoryRepository(categories=[category_film, category_series])
        category_to_update = copy.deepcopy(category_series)
        category_to_update.name = 'TV Series'
        category_to_update.description = 'Category for TV series'

        repository.update(category=category_to_update)

        assert len(repository.categories) == 2
        assert repository.categories[1] == category_series
        assert repository.categories[1].name == category_to_update.name
        assert repository.categories[1].description == category_to_update.description
        assert repository.categories[1].is_active == category_series.is_active

    def test_can_deactivate_category(self):
        category_film = Category(name='Films', description='Category for films', is_active=True)
        repository = InMemoryCategoryRepository(categories=[category_film])
        category_to_update = copy.deepcopy(category_film)
        category_to_update.is_active = False

        repository.update(category=category_to_update)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category_film
        assert repository.categories[0].is_active is False
        assert repository.categories[0].name == category_film.name
        assert repository.categories[0].description == category_film.description

    def test_can_activate_category(self):
        category_film = Category(name='Films', description='Category for films', is_active=False)
        repository = InMemoryCategoryRepository(categories=[category_film])
        category_to_update = copy.deepcopy(category_film)
        category_to_update.is_active = True

        repository.update(category=category_to_update)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category_film
        assert repository.categories[0].is_active is True
        assert repository.categories[0].name == category_film.name
        assert repository.categories[0].description == category_film.description

    def test_when_category_does_not_exist_then_no_effect(self):
        category_film = Category(name='Films', description='Category for films')
        repository = InMemoryCategoryRepository(categories=[category_film])
        category_to_update = Category(name='Documentaries', description='Category for documentaries')

        repository.update(category=category_to_update)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category_film
        assert repository.categories[0].name == category_film.name
        assert repository.categories[0].description == category_film.description
        assert repository.categories[0].is_active == category_film.is_active
