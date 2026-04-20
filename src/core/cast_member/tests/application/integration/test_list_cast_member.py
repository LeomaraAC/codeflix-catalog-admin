import pytest

from src.core._shared.application.list_response import ListResponse, ListOutputMeta
from src.core.cast_member.application.usecase.list_cast_member import ListCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


@pytest.fixture
def john() -> CastMember:
    return CastMember(name='John Doe', type=CastMemberType.ACTOR)


@pytest.fixture
def jane() -> CastMember:
    return CastMember(name='Jane Smith', type=CastMemberType.DIRECTOR)


@pytest.fixture
def anne() -> CastMember:
    return CastMember(name='Anne Doe', type=CastMemberType.ACTOR)


@pytest.fixture
def repository_with_data(john: CastMember, jane: CastMember, anne: CastMember) -> CastMemberRepository:
    return InMemoryCastMemberRepository(cast_members=[jane, john, anne])


class TestListCastMember:
    def test_when_no_cast_member_then_return_empty_list(self):
        repository = InMemoryCastMemberRepository()

        use_case = ListCastMember(repository=repository)
        response = use_case.execute(input=ListCastMember.Input())

        assert response == ListResponse[ListCastMember.CastMember](data=[],
                                                                   meta=ListOutputMeta(current_page=1, per_page=2,
                                                                                       total=0))

    def test_when_cast_member_exists_then_return__mapped_list(self, repository_with_data: InMemoryCastMemberRepository,
                                                              anne: CastMember, jane: CastMember):
        use_case = ListCastMember(repository=repository_with_data)
        response = use_case.execute(input=ListCastMember.Input())

        assert len(response.data) == 2
        assert response.data[0] == ListCastMember.CastMember(id=anne.id, name=anne.name, type=anne.type)
        assert response.data[1] == ListCastMember.CastMember(id=jane.id, name=jane.name, type=jane.type)
        assert response.meta == ListOutputMeta(current_page=1, per_page=2, total=3)

    def test_with_paginated_and_order_by_name(self, repository_with_data: InMemoryCastMemberRepository, jane: CastMember):
        use_case = ListCastMember(repository=repository_with_data)
        response = use_case.execute(input=ListCastMember.Input(order_by='type', current_page=2))

        assert len(response.data) == 1
        assert response.data[0] == ListCastMember.CastMember(id=jane.id, name=jane.name, type=jane.type)
        assert response.meta == ListOutputMeta(current_page=2, per_page=2, total=3)
