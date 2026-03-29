from unittest.mock import create_autospec
from uuid import UUID

import pytest

from src.core.cast_member.application.exceptions import InvalidCastMember
from src.core.cast_member.application.usecase.create_cast_member import CreateCastMemberUseCase
from src.core.cast_member.domain.cast_member import CastMemberType, CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@pytest.fixture
def mock_cast_member_repository() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)


class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self, mock_cast_member_repository: CastMemberRepository):
        from src.core.cast_member.application.usecase.create_cast_member import CreateCastMemberUseCase

        use_case = CreateCastMemberUseCase(repository=mock_cast_member_repository)
        input = CreateCastMemberUseCase.Input(name='John Doe', type=CastMemberType.ACTOR)
        output = use_case.execute(input)

        assert output is not None
        assert isinstance(output.id, UUID)
        assert mock_cast_member_repository.save.call_count == 1
        assert mock_cast_member_repository.save.called is True
        mock_cast_member_repository.save.assert_called_once_with(
            CastMember(id=output.id, name=input.name, type=input.type))

    def test_create_cast_member_with_invalid_type(self, mock_cast_member_repository: CastMemberRepository):
        use_case = CreateCastMemberUseCase(repository=mock_cast_member_repository)

        with pytest.raises(InvalidCastMember, match='type must be either ACTOR or DIRECTOR'):
            use_case.execute(input=CreateCastMemberUseCase.Input(name='John Doe', type='SCREENWRITER'))


    def test_create_cast_member_with_invalid_name(self, mock_cast_member_repository: CastMemberRepository):
        use_case = CreateCastMemberUseCase(repository=mock_cast_member_repository)

        with pytest.raises(InvalidCastMember, match='name cannot be empty'):
            use_case.execute(input=CreateCastMemberUseCase.Input(name='', type=CastMemberType.ACTOR))

    def test_create_cast_member_with_name_longer_than_255_characters(self, mock_cast_member_repository: CastMemberRepository):
        use_case = CreateCastMemberUseCase(repository=mock_cast_member_repository)
        with pytest.raises(InvalidCastMember, match='name cannot be longer than 255 characters'):
            use_case.execute(input=CreateCastMemberUseCase.Input(name='a' * 256, type=CastMemberType.ACTOR))