from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.exceptions import CastMemberNotFound, InvalidCastMember
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class UpdateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.cast_member_repository = repository

    @dataclass
    class Input:
        id: UUID
        name: str
        type: CastMemberType

    def execute(self, input: Input) -> None:
        cast_member = self.cast_member_repository.get_by_id(input.id)
        if not cast_member:
            raise CastMemberNotFound(f'Cast member with ID {input.id} not found')

        try:
            cast_member.update(name=input.name, type=input.type)
        except ValueError as e:
            raise InvalidCastMember(e)

        self.cast_member_repository.update(cast_member)