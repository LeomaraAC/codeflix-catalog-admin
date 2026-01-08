from rest_framework.test import APITestCase

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository


class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        category_films = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series', is_active=False)
        repository = DjangoORMCategoryRepository()
        repository.save(category_films)
        repository.save(category_series)


        response = self.client.get('/api/categories/')

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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, expected_data)