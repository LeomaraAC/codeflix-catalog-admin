import pytest
from rest_framework.test import APIClient




@pytest.fixture
def base_url() -> str:
    return '/api/cast_members/'


@pytest.mark.django_db
class TestCreateAndDeleteCastMember:
    def test_user_can_create_and_delete_cast_member(self, authenticated_client: APIClient, base_url: str) -> None:
        list_response = authenticated_client.get(base_url)
        assert list_response.data == {'data': [], 'meta': {'current_page': 1, 'per_page': 2, 'total': 0}}
        cast_member_to_create = {'name': 'John Doe', 'type': 'DIRECTOR'}

        # Cria um cast member
        create_response = authenticated_client.post(base_url, cast_member_to_create, format='json')

        assert create_response.status_code == 201
        created_cast_member_id = create_response.data['id']

        assert authenticated_client.get(base_url).data == {
            'data': [{'id': created_cast_member_id, **cast_member_to_create}],
            'meta': {'current_page': 1, 'per_page': 2, 'total': 1}
        }

        # Deleta cast member
        delete_response = authenticated_client.delete(f'{base_url}{created_cast_member_id}/')
        assert delete_response.status_code == 204

        # Verifica que a listagem está vazia novamente
        assert authenticated_client.get(base_url).data == {'data': [], 'meta': {'current_page': 1, 'per_page': 2, 'total': 0}}
