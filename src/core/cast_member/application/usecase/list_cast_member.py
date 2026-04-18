from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class ListCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.cast_member_repository = repository

    @dataclass
    class Input:
        order_by: str = 'name'

    @dataclass
    class Output:
        @dataclass
        class CastMember:
            id: UUID
            name: str
            type: CastMemberType

        data: list[CastMember]

    def execute(self, input: Input) -> Output:
        cast_members = self.cast_member_repository.list()
        cast_members_output = sorted(
            [self.Output.CastMember(id=cast_member.id, name=cast_member.name, type=cast_member.type)
             for cast_member in cast_members],
            key=lambda cast_member: (getattr(cast_member, input.order_by) is None, getattr(cast_member, input.order_by, ""))
        )
        return self.Output(data=cast_members_output)
