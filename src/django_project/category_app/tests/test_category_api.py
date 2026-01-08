from rest_framework.test import APITestCase

class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        response = self.client.get('/api/categories/')

        expected_data = [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Films",
                "description": "Category for films",
                "is_active": True
            },
            {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "Series",
                "description": "Category for series",
                "is_active": False
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, expected_data)