from unittest.mock import create_autospec

from src.core.cast_member.application.usecase.list_cast_member import ListCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestListCastMember:
    def test_when_no_cast_member_then_return_empty_list(self):
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.list.return_value = []

        use_case = ListCastMember(repository=mock_repository)
        response = use_case.execute(input=ListCastMember.Input())

        assert response == ListCastMember.Output(data=[])

    def test_when_cast_member_exists_then_return__mapped_list(self):
        john = CastMember(name='John Doe', type=CastMemberType.ACTOR)
        jane = CastMember(name='Jane Smith', type=CastMemberType.DIRECTOR)

        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.list.return_value = [john, jane]

        use_case = ListCastMember(repository=mock_repository)
        response = use_case.execute(input=ListCastMember.Input())


        assert len(response.data) == 2
        assert response == ListCastMember.Output(data=[
            ListCastMember.Output.CastMember(id=john.id, name=john.name, type=john.type),
            ListCastMember.Output.CastMember(id=jane.id, name=jane.name, type=jane.type),
        ])

