from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.list_response import ListResponse, ListOutputMeta
from src.core._shared.application.list_utils import ListUtils
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class ListCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.cast_member_repository = repository

    @dataclass
    class Input:
        order_by: str = 'name'
        current_page: int = 1

    @dataclass
    class CastMember:
        id: UUID
        name: str
        type: CastMemberType

    def execute(self, input: Input) -> ListResponse[CastMember]:
        cast_members = self.cast_member_repository.list()
        sorted_cast_members = ListUtils.sort(
            [self.CastMember(id=cast_member.id, name=cast_member.name, type=cast_member.type)
             for cast_member in cast_members], input.order_by)

        genres_page = ListUtils.paginate(sorted_cast_members, input.current_page)

        return ListResponse[self.CastMember](data=genres_page,
                                             meta=ListOutputMeta(current_page=input.current_page,
                                                                 per_page=ListUtils.DEFAULT_PAGE_SIZE,
                                                                 total=len(sorted_cast_members)))
