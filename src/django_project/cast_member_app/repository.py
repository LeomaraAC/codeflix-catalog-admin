from typing import List
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberORM


class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_member_orm: CastMemberORM = CastMemberORM) -> None:
        self.cast_member_orm = cast_member_orm

    def save(self, cast_member: CastMember) -> None:
        self.cast_member_orm.objects.create(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type
        )

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member_record = self.cast_member_orm.objects.get(id=id)
            return CastMember(
                id=cast_member_record.id,
                name=cast_member_record.name,
                type=cast_member_record.type
            )
        except self.cast_member_orm.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        self.cast_member_orm.objects.filter(id=id).delete()

    def update(self, cast_member: CastMember) -> None:
        self.cast_member_orm.objects.filter(pk=cast_member.id).update(
            name=cast_member.name,
            type=cast_member.type
        )

    def list(self) -> List[CastMember]:
        return [
            CastMember(
                id=record.id,
                name=record.name,
                type=record.type
            ) for record in self.cast_member_orm.objects.all()
        ]