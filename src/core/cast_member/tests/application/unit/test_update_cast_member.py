from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src.core.cast_member.application.exceptions import InvalidCastMember, CastMemberNotFound
from src.core.cast_member.application.usecase.update_cast_member import UpdateCastMember
from src.core.cast_member.domain.cast_member import CastMemberType, CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@pytest.fixture
def cast_member_repository() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)

@pytest.fixture
def cast_member_john() -> CastMember:
    return CastMember(name='John Doe', type=CastMemberType.ACTOR)


class TestUpdateCastMember:
    def test_when_cast_member_does_not_exist_then_return_not_found_exception(self, cast_member_repository: CastMemberRepository):
        cast_member_repository.get_by_id.return_value = None

        cast_member_id = uuid4()

        use_case = UpdateCastMember(repository=cast_member_repository)
        with pytest.raises(CastMemberNotFound, match='Cast member with ID .* not found'):
            use_case.execute(UpdateCastMember.Input(id=cast_member_id, name='John', type=CastMemberType.ACTOR))

        cast_member_repository.get_by_id.assert_called_once_with(id=cast_member_id)
        cast_member_repository.update.assert_not_called()

    def test_when_cast_member_name_is_invalid_then_return_exception(self, cast_member_repository: CastMemberRepository, cast_member_john: CastMember):
        cast_member_repository.get_by_id.return_value = cast_member_john

        use_case = UpdateCastMember(repository=cast_member_repository)

        input_data = UpdateCastMember.Input(id=cast_member_john.id, name='', type=cast_member_john.type)
        with pytest.raises(InvalidCastMember, match='name cannot be empty'):
            use_case.execute(input_data)

        cast_member_repository.get_by_id.assert_called_once_with(id=cast_member_john.id)

        input_data.name = 'a' * 256
        with pytest.raises(InvalidCastMember, match='name cannot be longer than 255 characters'):
            use_case.execute(input_data)

        cast_member_repository.update.assert_not_called()

    def test_when_cast_member_type_is_invalid_then_return_exception(self, cast_member_repository: CastMemberRepository, cast_member_john: CastMember):
        cast_member_repository.get_by_id.return_value = cast_member_john

        use_case = UpdateCastMember(repository=cast_member_repository)

        input_data = UpdateCastMember.Input(id=cast_member_john.id, name='Jane Doe', type='SCREENWRITER')
        with pytest.raises(InvalidCastMember, match='type must be either ACTOR or DIRECTOR'):
            use_case.execute(input_data)

        cast_member_repository.get_by_id.assert_called_once_with(id=cast_member_john.id)
        cast_member_repository.update.assert_not_called()



    def test_when_cast_member_is_valid_then_return_success(self, cast_member_repository: CastMemberRepository, cast_member_john: CastMember):
        cast_member_repository.get_by_id.return_value = cast_member_john

        use_case = UpdateCastMember(repository=cast_member_repository)
        input_data = UpdateCastMember.Input(id=cast_member_john.id, name='Jane Doe', type=CastMemberType.DIRECTOR)

        use_case.execute(input_data)

        cast_member_repository.get_by_id.assert_called_once_with(id=cast_member_john.id)
        cast_member_repository.update.assert_called_once()