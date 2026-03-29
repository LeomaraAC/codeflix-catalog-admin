from uuid import uuid4

import pytest

from src.core.cast_member.application.exceptions import InvalidCastMember, CastMemberNotFound
from src.core.cast_member.application.usecase.update_cast_member import UpdateCastMember
from src.core.cast_member.domain.cast_member import CastMemberType, CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


@pytest.fixture
def john() -> CastMember:
    return CastMember(name='John Doe', type=CastMemberType.DIRECTOR)


@pytest.fixture
def jane() -> CastMember:
    return CastMember(name='Jane Smith', type=CastMemberType.ACTOR)


@pytest.fixture
def repository_with_data(john: CastMember, jane: CastMember) -> CastMemberRepository:
    return InMemoryCastMemberRepository(cast_members=[jane, john])


class TestUpdateCastMember:
    def test_when_cast_member_does_not_exist_then_return_not_found_exception(self):
        use_case = UpdateCastMember(repository=InMemoryCastMemberRepository())
        with pytest.raises(CastMemberNotFound, match='Cast member with ID .* not found'):
            use_case.execute(UpdateCastMember.Input(id=uuid4(), name='John', type=CastMemberType.ACTOR))


    def test_when_cast_member_name_is_invalid_then_return_exception(self, repository_with_data: InMemoryCastMemberRepository, john: CastMember):
        use_case = UpdateCastMember(repository=repository_with_data)

        input_data = UpdateCastMember.Input(id=john.id, name='', type=john.type)
        with pytest.raises(InvalidCastMember, match='name cannot be empty'):
            use_case.execute(input_data)

        input_data.name = 'a' * 256
        with pytest.raises(InvalidCastMember, match='name cannot be longer than 255 characters'):
            use_case.execute(input_data)

        assert repository_with_data.cast_members[1].name == john.name

    def test_when_cast_member_type_is_invalid_then_return_exception(self, repository_with_data: InMemoryCastMemberRepository, john: CastMember):
        use_case = UpdateCastMember(repository=repository_with_data)

        input_data = UpdateCastMember.Input(id=john.id, name='Jane Doe', type='SCREENWRITER')
        with pytest.raises(InvalidCastMember, match='type must be either ACTOR or DIRECTOR'):
            use_case.execute(input_data)

        assert repository_with_data.cast_members[1].type == john.type

    def test_when_cast_member_is_valid_then_return_success(self, repository_with_data: InMemoryCastMemberRepository, john: CastMember):
        use_case = UpdateCastMember(repository=repository_with_data)
        input_data = UpdateCastMember.Input(id=john.id, name='Jane Doe', type=CastMemberType.ACTOR)

        use_case.execute(input_data)
        assert repository_with_data.cast_members[1].name == 'Jane Doe'
        assert repository_with_data.cast_members[1].type == CastMemberType.ACTOR
        assert repository_with_data.cast_members[1].id == john.id