from uuid import uuid4

import pytest

from src.django_project.cast_member_app.models import CastMember as CastMemberORM
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository

@pytest.fixture
def john():
    return CastMember(name='John Doe', type=CastMemberType.ACTOR)

@pytest.fixture
def jane():
    return CastMember(name='Jane Smith', type=CastMemberType.ACTOR)

@pytest.mark.django_db
class TestSave:
    def test_can_save_cast_member_in_database(self, john: CastMember):
        repository = DjangoORMCastMemberRepository()

        assert CastMemberORM.objects.count() == 0

        repository.save(john)
        assert CastMemberORM.objects.count() == 1
        saved_cast_member = CastMemberORM.objects.first()
        assert saved_cast_member.id == john.id
        assert saved_cast_member.name == john.name
        assert saved_cast_member.type == john.type

@pytest.mark.django_db
class TestGetById:
    def test_can_get_cast_member_by_id_from_database(self, john: CastMember):
        john_record = CastMemberORM.objects.create(id=john.id, name=john.name, type=john.type)
        repository = DjangoORMCastMemberRepository()

        cast_member = repository.get_by_id(id=john_record.id)

        assert cast_member is not None
        assert type(cast_member) == CastMember
        assert cast_member.id == john_record.id
        assert cast_member.name == john_record.name
        assert cast_member.type == john_record.type

    def test_when_cast_member_does_not_exist_then_return_none(self, john: CastMember):
        CastMemberORM.objects.create(id=john.id, name=john.name, type=john.type)
        repository = DjangoORMCastMemberRepository()
        not_found_id = uuid4()

        cast_member = repository.get_by_id(id=not_found_id)

        assert cast_member is None

@pytest.mark.django_db
class TestDelete:
    def test_can_delete_cast_member_by_id_from_database(self, john: CastMember, jane: CastMember):
        CastMemberORM.objects.create(id=john.id, name=john.name, type=john.type)
        CastMemberORM.objects.create(id=jane.id, name=jane.name, type=jane.type)

        repository = DjangoORMCastMemberRepository()
        assert CastMemberORM.objects.count() == 2

        repository.delete(id=john.id)
        assert CastMemberORM.objects.count() == 1

        cast_member_found = CastMemberORM.objects.first()
        assert cast_member_found.id == jane.id

    def test_when_cast_member_does_not_exist_then_no_effect(self, jane: CastMember):
        CastMemberORM.objects.create(id=jane.id, name=jane.name, type=jane.type)
        repository = DjangoORMCastMemberRepository()
        not_found_id = uuid4()

        assert CastMemberORM.objects.count() == 1

        repository.delete(id=not_found_id)

        assert CastMemberORM.objects.count() == 1

@pytest.mark.django_db
class TestUpdate:
    def test_can_update_cast_member_in_database(self, john: CastMember, jane: CastMember):
        CastMemberORM.objects.create(id=john.id, name=john.name, type=john.type)
        CastMemberORM.objects.create(id=jane.id, name=jane.name, type=jane.type)

        repository = DjangoORMCastMemberRepository()

        cast_member_to_update = CastMember(id=jane.id, name='Jane Doe', type=CastMemberType.DIRECTOR)

        repository.update(cast_member_to_update)
        updated_cast_member = CastMemberORM.objects.get(id=jane.id)

        assert updated_cast_member.id == cast_member_to_update.id
        assert updated_cast_member.name == cast_member_to_update.name
        assert updated_cast_member.type == cast_member_to_update.type

    def test_when_cast_member_does_not_exist_then_no_effect(self, john: CastMember):
        CastMemberORM.objects.create(id=john.id, name=john.name, type=john.type)
        repository = DjangoORMCastMemberRepository()
        not_found_id = uuid4()

        cast_member_to_update = CastMember(id=not_found_id, name='Non Existent', type=CastMemberType.ACTOR)

        repository.update(cast_member_to_update)

        existing_cast_member = CastMemberORM.objects.get(id=john.id)
        assert existing_cast_member.id == john.id
        assert existing_cast_member.name == john.name
        assert existing_cast_member.type == john.type

@pytest.mark.django_db
class TestList:
    def test_can_list_cast_members(self, john: CastMember, jane: CastMember):
        CastMemberORM.objects.create(id=john.id, name=john.name, type=john.type)
        CastMemberORM.objects.create(id=jane.id, name=jane.name, type=jane.type)

        repository = DjangoORMCastMemberRepository()
        cast_members = repository.list()

        assert len(cast_members) == 2
        assert john in cast_members
        assert jane in cast_members

    def test_when_no_cast_member_then_return_empty_list(self):
        repository = DjangoORMCastMemberRepository()
        cast_members = repository.list()

        assert len(cast_members) == 0



