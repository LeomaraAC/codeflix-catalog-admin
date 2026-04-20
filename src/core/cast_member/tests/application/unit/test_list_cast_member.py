from unittest.mock import create_autospec

from src.core._shared.application.list_response import ListResponse, ListOutputMeta
from src.core.cast_member.application.usecase.list_cast_member import ListCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestListCastMember:
    def test_when_no_cast_member_then_return_empty_list(self):
        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.list.return_value = []

        use_case = ListCastMember(repository=mock_repository)
        response = use_case.execute(input=ListCastMember.Input())

        assert response == ListResponse[ListCastMember.CastMember](data=[], meta=ListOutputMeta(current_page=1, per_page=2, total=0))

    def test_when_cast_member_exists_then_return__mapped_list(self):
        john = CastMember(name='John Doe', type=CastMemberType.ACTOR)
        jane = CastMember(name='Jane Smith', type=CastMemberType.DIRECTOR)

        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.list.return_value = [john, jane]

        use_case = ListCastMember(repository=mock_repository)
        response = use_case.execute(input=ListCastMember.Input())


        assert len(response.data) == 2
        assert response == ListResponse[ListCastMember.CastMember](data=[
            ListCastMember.CastMember(id=jane.id, name=jane.name, type=jane.type),
            ListCastMember.CastMember(id=john.id, name=john.name, type=john.type),
        ], meta=ListOutputMeta(current_page=1, per_page=2, total=2))

    def test_when_order_by_type_then_return_ordered_list(self):
        john = CastMember(name='John Doe', type=CastMemberType.DIRECTOR)
        jane = CastMember(name='Jane Smith', type=CastMemberType.ACTOR)

        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.list.return_value = [john, jane]

        use_case = ListCastMember(repository=mock_repository)
        response = use_case.execute(input=ListCastMember.Input(order_by='type'))

        assert len(response.data) == 2
        assert response == ListResponse[ListCastMember.CastMember](data=[
            ListCastMember.CastMember(id=jane.id, name=jane.name, type=jane.type),
            ListCastMember.CastMember(id=john.id, name=john.name, type=john.type),
        ], meta=ListOutputMeta(current_page=1, per_page=2, total=2))

    def test_when_pagination_then_return_paginated_list(self):
        cast_members = [CastMember(name=f'Cast Member {i}', type=CastMemberType.ACTOR) for i in range(5)]

        mock_repository = create_autospec(CastMemberRepository)
        mock_repository.list.return_value = cast_members

        use_case = ListCastMember(repository=mock_repository)
        response = use_case.execute(input=ListCastMember.Input(current_page=2))

        assert len(response.data) == 2
        assert response == ListResponse[ListCastMember.CastMember](data=[
            ListCastMember.CastMember(id=cast_members[2].id, name=cast_members[2].name, type=cast_members[2].type),
            ListCastMember.CastMember(id=cast_members[3].id, name=cast_members[3].name, type=cast_members[3].type),
        ], meta=ListOutputMeta(current_page=2, per_page=2, total=5))

