import uuid

import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.fixture
def jane() -> CastMember:
    return CastMember(name='Jane Smith', type=CastMemberType.ACTOR)


@pytest.fixture
def john() -> CastMember:
    return CastMember(name='John Doe', type=CastMemberType.DIRECTOR)

@pytest.fixture
def samantha() -> CastMember:
    return CastMember(name='Samantha', type=CastMemberType.ACTOR)


@pytest.mark.django_db
class TestCreateCastMemberAPI:
    def test_when_payload_is_valid_than_return_201(self, repository: DjangoORMCastMemberRepository):
        payload = {'name': 'John Smith', 'type': 'ACTOR'}
        response = APIClient().post('/api/cast_members/', data=payload, format='json')

        assert response.status_code == HTTP_201_CREATED
        assert 'id' in response.data

        cast_member_created = repository.get_by_id(response.data['id'])
        assert cast_member_created is not None
        assert cast_member_created.name == payload['name']
        assert cast_member_created.type == payload['type']

    def test_when_name_is_empty_than_return_400(self, repository: DjangoORMCastMemberRepository):
        payload = {'name': '', 'type': 'ACTOR'}
        response = APIClient().post('/api/cast_members/', data=payload, format='json')

        assert response.status_code == 400
        assert 'name' in response.data

    def test_when_name_is_invalid_than_return_400(self, repository: DjangoORMCastMemberRepository):
        payload = {'name': 'a' * 256, 'type': 'ACTOR'}
        response = APIClient().post('/api/cast_members/', data=payload, format='json')

        assert response.status_code == 400
        assert 'name' in response.data

    def test_when_type_is_invalid_than_return_400(self, repository: DjangoORMCastMemberRepository):
        payload = {'name': 'Jane Doe', 'type': 'SCREENWRITER'}
        response = APIClient().post('/api/cast_members/', data=payload, format='json')

        assert response.status_code == 400
        assert 'type' in response.data

    def test_payload_without_type_than_return_400(self, repository: DjangoORMCastMemberRepository):
        payload = {'name': 'Jane Doe'}
        response = APIClient().post('/api/cast_members/', data=payload, format='json')

        assert response.status_code == 400
        assert 'type' in response.data


@pytest.mark.django_db
class TestUpdateCastMemberAPI:
    def test_when_payload_is_valid_then_update_cast_member(self, repository: DjangoORMCastMemberRepository, jane: CastMember):
        repository.save(jane)

        payload = {'name': 'Jane Doe', 'type': 'DIRECTOR'}
        response = APIClient().put(f'/api/cast_members/{jane.id}/', data=payload, format='json')

        assert response.status_code == HTTP_204_NO_CONTENT

        updated_cast_member = repository.get_by_id(jane.id)
        assert updated_cast_member is not None
        assert updated_cast_member.name == payload['name']
        assert updated_cast_member.type == payload['type']

    def test_when_payload_is_invalid_then_return_400(self, repository: DjangoORMCastMemberRepository, jane: CastMember):
        repository.save(jane)

        payload = {'name': '', 'type': 'DIRECTOR'}
        response = APIClient().put(f'/api/cast_members/{jane.id}/', data=payload, format='json')

        assert response.status_code == 400
        assert 'name' in response.data

        payload = {'name': 'Jane', 'type': 'SCREENWRITER'}
        response = APIClient().put(f'/api/cast_members/{jane.id}/', data=payload, format='json')

        assert response.status_code == 400
        assert 'type' in response.data

    def test_when_cast_member_does_not_exist_then_return_404(self, repository: DjangoORMCastMemberRepository):
        payload = {'name': 'Jane', 'type': 'DIRECTOR'}
        response = APIClient().put(f'/api/cast_members/{str(uuid.uuid4())}/', data=payload, format='json')

        assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteCastMemberAPI:
    def test_delete_cast_member(self, repository: DjangoORMCastMemberRepository, jane: CastMember, john: CastMember):
        repository.save(jane)
        repository.save(john)

        response = APIClient().delete(f'/api/cast_members/{jane.id}/')
        assert response.status_code == HTTP_204_NO_CONTENT
        assert repository.get_by_id(jane.id) is None
        assert repository.get_by_id(john.id) is not None

    def test_when_cast_member_does_not_exist_then_return_404(self, repository: DjangoORMCastMemberRepository, jane: CastMember):
        repository.save(jane)

        response = APIClient().delete(f'/api/cast_members/{str(uuid.uuid4())}/')
        assert response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestListCastMemberAPI:
    def test_list_cast_members(self, repository: DjangoORMCastMemberRepository, jane: CastMember, john: CastMember):
        repository.save(jane)
        repository.save(john)

        response = APIClient().get('/api/cast_members/')

        assert response.status_code == HTTP_200_OK
        assert len(response.data['data']) == 2

        jane_data = response.data['data'][0]
        john_data = response.data['data'][1]

        assert jane_data['id'] == str(jane.id)
        assert jane_data['name'] == jane.name
        assert jane_data['type'] == jane.type

        assert john_data['id'] == str(john.id)
        assert john_data['name'] == john.name
        assert john_data['type'] == john.type

        assert response.data['meta'] == {'current_page': 1, 'per_page': 2, 'total': 2}

    def test_list_empty_cast_members(self, repository: DjangoORMCastMemberRepository):
        response = APIClient().get('/api/cast_members/')
        assert response.status_code == HTTP_200_OK
        assert len(response.data['data']) == 0
        assert response.data['meta'] == {'current_page': 1, 'per_page': 2, 'total': 0}

    def test_list_sorted_by_type_and_paginated(self, repository: DjangoORMCastMemberRepository, jane: CastMember, john: CastMember, samantha: CastMember):
        repository.save(john)
        repository.save(jane)
        repository.save(samantha)

        response = APIClient().get('/api/cast_members/?order_by=type&current_page=2')

        assert response.status_code == HTTP_200_OK
        assert response.data['meta'] == {'current_page': 2, 'per_page': 2, 'total': 3}
        assert len(response.data['data']) == 1

        john_data = response.data['data'][0]

        assert john_data['id'] == str(john.id)
        assert john_data['name'] == john.name
        assert john_data['type'] == john.type