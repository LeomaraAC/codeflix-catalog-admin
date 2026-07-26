import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCreateVideoErrors:
    def test_user_cannot_create_video_when_related_entities_do_not_exist(self, api_client: APIClient) -> None:
        create_video_response = api_client.post(
            '/api/videos/',
            {
                'title': 'John Wick',
                'description': 'Action movie',
                'launch_year': 2014,
                'duration': '120.50',
                'rating': 'AGE_16',
                'categories': ['95d0df35-0dbf-4e5d-a7e8-ee4fdf99597b'],
                'genres': ['e76ce838-fc0c-45a7-a164-ed5685686a4b'],
                'cast_members': ['dbd50345-dab7-4e93-8452-07a90c7c92ec'],
            },
            format='json',
        )

        assert create_video_response.status_code == 400
        assert 'Categories with provided IDs not found' in create_video_response.data['error']
        assert 'Genres with provided IDs not found' in create_video_response.data['error']
        assert 'Cast members with provided IDs not found' in create_video_response.data['error']