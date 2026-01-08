import pytest
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.mark.django_db
class TestCategoryAPI:

    @pytest.fixture
    def category_films(self) -> Category:
        return Category(name='Films', description='Category for films')

    @pytest.fixture
    def category_series(self) -> Category:
        return Category(name='Series', description='Category for series', is_active=False)

    @pytest.fixture
    def repository(self) -> DjangoORMCategoryRepository:
        return DjangoORMCategoryRepository()

    def test_list_categories(self, category_films: Category, category_series: Category, repository: DjangoORMCategoryRepository):
        repository.save(category_films)
        repository.save(category_series)


        response = APIClient().get('/api/categories/')

        expected_data = [
            {
                "id": str(category_films.id),
                "name": category_films.name,
                "description": category_films.description,
                "is_active": category_films.is_active
            },
            {
                "id": str(category_series.id),
                "name": category_series.name,
                "description": category_series.description,
                "is_active": category_series.is_active
            }
        ]

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data == expected_data