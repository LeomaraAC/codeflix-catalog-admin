import uuid
from unittest.mock import create_autospec
import pytest

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.application.usecase.delete_cast_member import DeleteCastMember
from src.core.cast_member.domain.cast_member import CastMemberType, CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(self):
        mock_cast_member = CastMember(name='Jane Smith', type=CastMemberType.ACTOR)
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = mock_cast_member

        use_case = DeleteCastMember(repository=mock_repository)
        use_case.execute(input=DeleteCastMember.Input(id=mock_cast_member.id))
        mock_repository.get_by_id.assert_called_once_with(mock_cast_member.id)
        mock_repository.delete.assert_called_once_with(mock_cast_member.id)


    def test_when_cast_member_not_found_then_raise_exception(self):
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.get_by_id.return_value = None
        cast_member_id = uuid.uuid4()

        use_case = DeleteCastMember(repository=mock_repository)
        with pytest.raises(CastMemberNotFound):
            use_case.execute(input=DeleteCastMember.Input(id=cast_member_id))

        mock_repository.get_by_id.assert_called_once_with(cast_member_id)
        mock_repository.delete.assert_not_called()
