import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def base_url() -> str:
    return '/api/categories/'


@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self, api_client: APIClient, base_url: str) -> None:
        # Acessa listagem e verifica que não tem nenhuma categoria criada
        list_response = api_client.get(base_url)
        assert list_response.data == {'data': []}

        # Cria uma categoria
        create_response = api_client.post(
            base_url,
            {
                'name': 'Movie',
                'description': 'Movie description',
            },
        )
        assert create_response.status_code == 201
        created_category_id = create_response.data['id']

        # Verifica que categoria criada aparece na listagem
        assert api_client.get(base_url).data == {
            'data': [
                {
                    'id': created_category_id,
                    'name': 'Movie',
                    'description': 'Movie description',
                    'is_active': True,
                }
            ]
        }

        # Edita categoria criada
        edit_response = api_client.put(
            f'/api/categories/{created_category_id}/',
            {
                'name': 'Documentary',
                'description': 'Documentary description',
                'is_active': True,
            },
        )
        assert edit_response.status_code == 204

        # Verifica que categoria editada aparece na listagem
        assert api_client.get(base_url).data == {
            'data': [
                {
                    'id': created_category_id,
                    'name': 'Documentary',
                    'description': 'Documentary description',
                    'is_active': True,
                }
            ]
        }

    def test_user_can_create_and_delete_category(self, api_client: APIClient, base_url: str) -> None:
        # Acessa listagem e verifica que não tem nenhuma categoria criada
        list_response = api_client.get(base_url)
        assert list_response.data == {'data': []}

        # Cria uma categoria
        create_response = api_client.post(
            base_url,
            {
                'name': 'Music',
                'description': 'Music description',
            },
        )
        assert create_response.status_code == 201
        created_category_id = create_response.data['id']

        # Verifica que categoria criada aparece na listagem
        assert api_client.get(base_url).data == {
            'data': [
                {
                    'id': created_category_id,
                    'name': 'Music',
                    'description': 'Music description',
                    'is_active': True,
                }
            ]
        }

        # Deleta categoria criada
        delete_response = api_client.delete(f'/api/categories/{created_category_id}/')
        assert delete_response.status_code == 204

        # Verifica que a listagem está vazia novamente
        assert api_client.get(base_url).data == {'data': []}
