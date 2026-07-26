import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCreateVideo:
    def test_user_can_create_video_with_related_entities(self, api_client: APIClient) -> None:
        category_response = api_client.post(
            '/api/categories/',
            {
                'name': 'Movie',
                'description': 'Movie category',
            },
            format='json',
        )
        genre_response = api_client.post(
            '/api/genres/',
            {
                'name': 'Action',
                'category_ids': [category_response.data['id']],
            },
            format='json',
        )
        cast_member_response = api_client.post(
            '/api/cast_members/',
            {
                'name': 'Keanu Reeves',
                'type': 'ACTOR',
            },
            format='json',
        )

        create_video_response = api_client.post(
            '/api/videos/',
            {
                'title': 'John Wick',
                'description': 'Action movie',
                'launch_year': 2014,
                'duration': '120.50',
                'rating': 'AGE_16',
                'categories': [category_response.data['id']],
                'genres': [genre_response.data['id']],
                'cast_members': [cast_member_response.data['id']],
            },
            format='json',
        )

        assert create_video_response.status_code == 201
        assert create_video_response.data['id']

        get_video_response = api_client.get(f"/api/videos/{create_video_response.data['id']}/")

        assert get_video_response.status_code == 200
        assert get_video_response.data == {
            'data': {
                'id': create_video_response.data['id'],
                'title': 'John Wick',
                'description': 'Action movie',
                'launch_year': 2014,
                'duration': '120.50',
                'published': False,
                'rating': 'AGE_16',
                'categories': [category_response.data['id']],
                'genres': [genre_response.data['id']],
                'cast_members': [cast_member_response.data['id']],
            }
        }
