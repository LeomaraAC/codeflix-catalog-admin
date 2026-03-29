from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class DeleteCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.cast_member_repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        cast_member = self.cast_member_repository.get_by_id(input.id)
        if not cast_member:
            raise CastMemberNotFound(f'Cast member with ID {input.id} not found')

        self.cast_member_repository.delete(id = input.id)