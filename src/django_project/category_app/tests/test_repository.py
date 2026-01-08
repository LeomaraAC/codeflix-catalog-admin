from uuid import uuid4

import pytest

from src.core.category.domain.category import Category
from django_project.category_app.models import Category as CategoryModel

from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.mark.django_db
class TestSave:
    def test_can_save_category_in_database(self):
        category = Category(name='Series', description='Category for series')
        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0

        repository.save(category)

        assert CategoryModel.objects.count() == 1
        saved_category = CategoryModel.objects.first()
        assert saved_category.id == category.id
        assert saved_category.name == category.name
        assert saved_category.description == category.description
        assert saved_category.is_active == category.is_active

@pytest.mark.django_db
class TestGetById:
    def test_can_get_category_by_id_from_database(self):
        category_record = CategoryModel.objects.create(
            name='Films',
            description='Category for films',
            is_active=True
        )
        repository = DjangoORMCategoryRepository()

        category = repository.get_by_id(id=category_record.id)

        assert category is not None
        assert type(category) == Category
        assert category.id == category_record.id
        assert category.name == category_record.name
        assert category.description == category_record.description
        assert category.is_active == category_record.is_active

    def test_when_category_does_not_exist_then_return_none(self):
        repository = DjangoORMCategoryRepository()
        not_found_id = uuid4()

        category = repository.get_by_id(id=not_found_id)

        assert category is None

@pytest.mark.django_db
class TestDelete:
    def test_can_delete_category_by_id_from_database(self):
        category_film_record = CategoryModel.objects.create(
            name='Films',
            description='Category for films',
            is_active=True
        )

        category_documentary_record = CategoryModel.objects.create(
            name='Documentaries',
            description='Category for documentaries',
            is_active=True
        )

        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 2

        repository.delete(id=category_film_record.id)

        category_found = CategoryModel.objects.first()

        assert CategoryModel.objects.count() == 1
        assert category_found.id == category_documentary_record.id

    def test_when_category_does_not_exist_then_no_effect(self):
        CategoryModel.objects.create(
            name='Films',
            description='Category for films',
            is_active=True
        )
        repository = DjangoORMCategoryRepository()
        not_found_id = uuid4()

        assert CategoryModel.objects.count() == 1

        repository.delete(id=not_found_id)

        assert CategoryModel.objects.count() == 1

@pytest.mark.django_db
class TestUpdate:
    def test_can_update_category_in_database(self):
        category_record = CategoryModel.objects.create(
            name='Films',
            description='Category for films',
            is_active=True
        )
        repository = DjangoORMCategoryRepository()

        category_to_update = Category(
            id=category_record.id,
            name='Documentaries',
            description='Category for documentaries',
            is_active=False
        )

        repository.update(category=category_to_update)

        updated_record = CategoryModel.objects.get(id=category_record.id)

        assert updated_record.name == category_to_update.name
        assert updated_record.description == category_to_update.description
        assert updated_record.is_active == category_to_update.is_active

    def test_when_category_does_not_exist_then_no_effect(self):
        category_record = CategoryModel.objects.create(
            name='Films',
            description='Category for films',
            is_active=True
        )
        repository = DjangoORMCategoryRepository()
        not_found_id = uuid4()

        category_to_update = Category(
            id=not_found_id,
            name='Nonexistent Category',
            description='This category does not exist',
            is_active=True
        )

        assert CategoryModel.objects.count() == 1

        repository.update(category=category_to_update)

        category_found = CategoryModel.objects.first()

        assert CategoryModel.objects.count() == 1
        assert category_found.id == category_record.id
        assert category_found.name == category_record.name
        assert category_found.description == category_record.description
        assert category_found.is_active == category_record.is_active

@pytest.mark.django_db
class TestList:
    def test_can_list_all_categories_from_database(self):
        category_film_record = CategoryModel.objects.create(
            name='Films',
            description='Category for films',
            is_active=True
        )

        category_series_record = CategoryModel.objects.create(
            name='Series',
            description='Category for series',
            is_active=False
        )

        repository = DjangoORMCategoryRepository()

        categories = repository.list()

        assert len(categories) == 2

        category_film = next((cat for cat in categories if cat.id == category_film_record.id), None)
        category_series = next((cat for cat in categories if cat.id == category_series_record.id), None)

        assert category_film is not None
        assert category_film.name == category_film_record.name
        assert category_film.description == category_film_record.description
        assert category_film.is_active == category_film_record.is_active

        assert category_series is not None
        assert category_series.name == category_series_record.name
        assert category_series.description == category_series_record.description
        assert category_series.is_active == category_series_record.is_active

    def test_when_no_categories_exist_then_return_empty_list(self):
        repository = DjangoORMCategoryRepository()

        categories = repository.list()

        assert len(categories) == 0
