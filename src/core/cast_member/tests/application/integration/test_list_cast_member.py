import pytest

from src.core.cast_member.application.usecase.list_cast_member import ListCastMember
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
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


class TestListCastMember:
    def test_when_no_cast_member_then_return_empty_list(self):
        repository = InMemoryCastMemberRepository()

        use_case = ListCastMember(repository=repository)
        response = use_case.execute(input=ListCastMember.Input())

        assert response == ListCastMember.Output(data=[])

    def test_when_cast_member_exists_then_return__mapped_list(self, repository_with_data: InMemoryCastMemberRepository,
                                                              john: CastMember, jane: CastMember):
        use_case = ListCastMember(repository=repository_with_data)
        response = use_case.execute(input=ListCastMember.Input())

        assert len(response.data) == 2
        assert ListCastMember.Output.CastMember(id=john.id, name=john.name, type=john.type) in response.data
        assert ListCastMember.Output.CastMember(id=jane.id, name=jane.name, type=jane.type) in response.data
