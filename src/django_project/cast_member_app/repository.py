from typing import List
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberORM


class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_member_orm: CastMemberORM = CastMemberORM) -> None:
        self.cast_member_orm = cast_member_orm

    def save(self, cast_member: CastMember) -> None:
        cast_member_model = CastMemberModelMapper.to_model_orm(cast_member)
        cast_member_model.save()

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cast_member_record = self.cast_member_orm.objects.get(id=id)
            return CastMemberModelMapper.to_entity(cast_member_record)
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
            CastMemberModelMapper.to_entity(record)
            for record in self.cast_member_orm.objects.all()
        ]


class CastMemberModelMapper:
    @staticmethod
    def to_model_orm(cast_member: CastMember) -> CastMemberORM:
        return CastMemberORM(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )

    @staticmethod
    def to_entity(cast_member: CastMemberORM) -> CastMember:
        return CastMember(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )