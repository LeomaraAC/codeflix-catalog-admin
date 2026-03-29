import uuid
import pytest

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.application.usecase.delete_cast_member import DeleteCastMember
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


class TestDeleteCastMember:
    def test_delete_cast_member_from_repository(self, repository_with_data: InMemoryCastMemberRepository, john: CastMember):

        use_case = DeleteCastMember(repository=repository_with_data)
        use_case.execute(input=DeleteCastMember.Input(id=john.id))

        assert len(repository_with_data.cast_members) == 1
        assert john not in repository_with_data.cast_members

    def test_when_cast_member_not_found_then_raise_exception(self, repository_with_data: InMemoryCastMemberRepository):
        use_case = DeleteCastMember(repository=repository_with_data)
        with pytest.raises(CastMemberNotFound):
            use_case.execute(input=DeleteCastMember.Input(id=uuid.uuid4()))

        assert len(repository_with_data.cast_members) == 2
