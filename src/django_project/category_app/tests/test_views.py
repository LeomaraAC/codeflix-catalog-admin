from uuid import uuid4, UUID

import pytest
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
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
