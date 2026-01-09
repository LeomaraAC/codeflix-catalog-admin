from uuid import uuid4, UUID

import pytest
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, \
    HTTP_204_NO_CONTENT
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.fixture
def category_films() -> Category:
    return Category(name='Films', description='Category for films')


@pytest.fixture
def category_series() -> Category:
    return Category(name='Series', description='Category for series', is_active=False)


@pytest.fixture
def repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestListCategoryAPI:
    def test_list_categories(self, category_films: Category, category_series: Category,
                             repository: DjangoORMCategoryRepository):
        repository.save(category_films)
        repository.save(category_series)

        response = APIClient().get('/api/categories/')

        expected_data = {
            'data': [
                {
                    'id': str(category_films.id),
                    'name': category_films.name,
                    'description': category_films.description,
                    'is_active': category_films.is_active
                },
                {
                    'id': str(category_series.id),
                    'name': category_series.name,
                    'description': category_series.description,
                    'is_active': category_series.is_active
                }
            ]
        }

        assert response.status_code == HTTP_200_OK
        assert len(response.data['data']) == 2
        assert response.data == expected_data


@pytest.mark.django_db
class TestRetrieveCategoryAPI:
    def test_when_invalid_uuid_then_return_400(self):
        response = APIClient().get('/api/categories/123123/')

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_return_category_by_id(self, category_films: Category, category_series: Category,
                                   repository: DjangoORMCategoryRepository):
        repository.save(category_films)
        repository.save(category_series)

        response = APIClient().get(f'/api/categories/{category_films.id}/')

        expected_data = {
            'data': {
                'id': str(category_films.id),
                'name': category_films.name,
                'description': category_films.description,
                'is_active': category_films.is_active
            }
        }

        assert response.status_code == HTTP_200_OK
        assert response.data == expected_data

    def test_return_404_when_category_not_found(self):
        response = APIClient().get(f'/api/categories/{uuid4()}/')

        assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateCategoryAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        payload = {
            'name': '',
            'description': 'Category for documentaries'
        }

        response = APIClient().post('/api/categories/', data=payload, format='json')

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert 'name' in response.data

    def test_when_description_is_missing_then_create_category(self, repository: DjangoORMCategoryRepository):
        payload = {
            'name': 'Documentaries'
        }

        response = APIClient().post('/api/categories/', data=payload, format='json')

        assert response.status_code == HTTP_201_CREATED
        assert 'id' in response.data

        category_created = repository.get_by_id(UUID(response.data['id']))

        assert payload['name'] == category_created.name
        assert not category_created.description

    def test_when_payload_is_valid_than_return_201(self, repository: DjangoORMCategoryRepository):
        payload = {
            'name': 'Documentaries',
            'description': 'Category for documentaries',
            'is_active': True
        }

        response = APIClient().post('/api/categories/', data=payload, format='json')

        assert response.status_code == HTTP_201_CREATED
        assert 'id' in response.data

        created_category_id = UUID(response.data['id'])
        category_created = repository.get_by_id(UUID(response.data['id']))
        expected_category = Category(id=created_category_id, **payload)

        assert expected_category == category_created
        assert repository.list() == [expected_category]


@pytest.mark.django_db
class TestUpdateCategoryAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        payload = {
            'name': '',  # invalid name
            'description': 'Updated description'
            # is_active is missing
        }
        url = '/api/categories/1234/'  # invalid UUID

        response = APIClient().put(url, data=payload)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {'name': ['This field may not be blank.'], 'id': ['Must be a valid UUID.'],
                                 'is_active': ['This field is required.']}

    def test_when_payload_is_valid_then_return_204(self, category_films: Category,
                                                   repository: DjangoORMCategoryRepository):
        repository.save(category_films)

        payload = {
            'name': 'Film',
            'description': 'Updated description',
            'is_active': True
        }

        response = APIClient().put(f'/api/categories/{category_films.id}/', data=payload)

        assert response.status_code == HTTP_204_NO_CONTENT

        updated_category = repository.get_by_id(category_films.id)

        assert updated_category.name == payload['name']
        assert updated_category.description == payload['description']
        assert updated_category.is_active is True

    def test_when_category_not_found_then_return_404(self):
        payload = {
            'name': 'Nonexistent Category',
            'description': 'This category does not exist',
            'is_active': True
        }

        response = APIClient().put(f'/api/categories/{uuid4()}/', data=payload)

        assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteCategoryAPI:
    def test_when_id_invalid_uuid_then_return_400(self):
        response = APIClient().delete('/api/categories/invalid-uuid/')

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_when_category_does_exist_then_delete_and_return_204(self, category_series: Category,
                                                                 repository: DjangoORMCategoryRepository):
        repository.save(category_series)

        response = APIClient().delete(f'/api/categories/{category_series.id}/')

        assert response.status_code == HTTP_204_NO_CONTENT
        assert repository.get_by_id(category_series.id) is None

    def test_when_category_not_found_then_return_404(self):
        response = APIClient().delete(f'/api/categories/{uuid4()}/')

        assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPartialUpdateCategoryAPI:
    def test_can_update_name_only(self, category_films: Category, repository: DjangoORMCategoryRepository):
        repository.save(category_films)
        payload = {
            'name': 'Updated Films Name'
        }

        response = APIClient().patch(f'/api/categories/{category_films.id}/', data=payload)
        assert response.status_code == HTTP_204_NO_CONTENT
        updated_category = repository.get_by_id(category_films.id)
        assert updated_category.name == payload['name']  # updated
        assert updated_category.description == category_films.description  # unchanged
        assert updated_category.is_active == category_films.is_active  # unchanged

    def test_can_update_description_only(self, category_films: Category,
                                         repository: DjangoORMCategoryRepository):
        repository.save(category_films)

        payload = {
            'description': 'Partially updated description'
        }

        response = APIClient().patch(f'/api/categories/{category_films.id}/', data=payload)

        assert response.status_code == HTTP_204_NO_CONTENT

        updated_category = repository.get_by_id(category_films.id)

        assert updated_category.name == category_films.name  # unchanged
        assert updated_category.description == payload['description']  # updated
        assert updated_category.is_active == category_films.is_active  # unchanged

    def test_can_update_is_active_only(self, category_series: Category,
                                       repository: DjangoORMCategoryRepository):
        repository.save(category_series)

        payload = {
            'is_active': True
        }

        response = APIClient().patch(f'/api/categories/{category_series.id}/', data=payload)

        assert response.status_code == HTTP_204_NO_CONTENT

        updated_category = repository.get_by_id(category_series.id)

        assert updated_category.name == category_series.name  # unchanged
        assert updated_category.description == category_series.description  # unchanged
        assert updated_category.is_active == payload['is_active']  # updated

    def test_can_update_name_and_description(self, category_films: Category,
                                             repository: DjangoORMCategoryRepository):
        repository.save(category_films)

        payload = {
            'name': 'New Name',
            'description': 'New Description'
        }

        response = APIClient().patch(f'/api/categories/{category_films.id}/', data=payload)

        assert response.status_code == HTTP_204_NO_CONTENT

        updated_category = repository.get_by_id(category_films.id)

        assert updated_category.name == payload['name']  # updated
        assert updated_category.description == payload['description']  # updated
        assert updated_category.is_active == category_films.is_active  # unchanged

    def test_when_category_not_found_then_return_404(self):
        payload = {
            'name': 'Nonexistent Category'
        }

        response = APIClient().patch(f'/api/categories/{uuid4()}/', data=payload)

        assert response.status_code == HTTP_404_NOT_FOUND

    def test_when_payload_is_empty_then_do_nothing(self, category_films: Category,
                                                   repository: DjangoORMCategoryRepository):
        repository.save(category_films)

        payload = {}

        response = APIClient().patch(f'/api/categories/{category_films.id}/', data=payload)

        assert response.status_code == HTTP_204_NO_CONTENT

        updated_category = repository.get_by_id(category_films.id)

        assert updated_category.id == category_films.id
        assert updated_category.name == category_films.name
        assert updated_category.description == category_films.description
        assert updated_category.is_active == category_films.is_active
