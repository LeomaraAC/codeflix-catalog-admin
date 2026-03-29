from typing import List, Optional
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class InMemoryCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_members: List[CastMember] = None):
        self.cast_members = cast_members or []

    def save(self, cast_member):
        self.cast_members.append(cast_member)

    def get_by_id(self, id: UUID) -> Optional[CastMember]:
        return next((cast_member for cast_member in self.cast_members if cast_member.id == id), None)

    def delete(self, id: UUID) -> None:
        cast_member = self.get_by_id(id)
        if not cast_member:
            return
        self.cast_members.remove(cast_member)

    def update(self, cast_member: CastMember) -> None:
        if not cast_member in self.cast_members:
            return
        index = self.cast_members.index(cast_member)
        self.cast_members[index] = cast_member

    def list(self) -> List[CastMember]:
        return [category for category in self.cast_members]
