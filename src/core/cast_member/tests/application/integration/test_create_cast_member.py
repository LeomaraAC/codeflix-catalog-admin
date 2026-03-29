from uuid import UUID

import pytest

from src.core.cast_member.application.exceptions import InvalidCastMember
from src.core.cast_member.application.usecase.create_cast_member import CreateCastMember
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self):
        repository = InMemoryCastMemberRepository()

        use_case = CreateCastMember(repository=repository)
        input = CreateCastMember.Input(name='John Doe', type=CastMemberType.ACTOR)
        output = use_case.execute(input)

        assert output is not None
        assert isinstance(output.id, UUID)
        assert len(repository.cast_members) == 1
        persisted_cast_member = repository.cast_members[0]
        assert persisted_cast_member.id == output.id
        assert persisted_cast_member.name == input.name
        assert persisted_cast_member.type == input.type

    def test_create_cast_member_with_invalid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)

        with pytest.raises(InvalidCastMember, match='name cannot be empty'):
            use_case.execute(input=CreateCastMember.Input(name='', type=CastMemberType.ACTOR))
        assert len(repository.cast_members) == 0

        with pytest.raises(InvalidCastMember, match='name cannot be longer than 255 characters'):
            use_case.execute(input=CreateCastMember.Input(name='a' * 256, type=CastMemberType.ACTOR))
        assert len(repository.cast_members) == 0

        with pytest.raises(InvalidCastMember, match='type must be either ACTOR or DIRECTOR'):
            use_case.execute(input=CreateCastMember.Input(name='John Doe', type='SCREENWRITER'))
        assert len(repository.cast_members) == 0
