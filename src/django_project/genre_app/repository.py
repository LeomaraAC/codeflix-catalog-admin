from typing import List
from uuid import UUID

from django.db import transaction

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import Genre as GenreORM


class DjangoORMGenreRepository(GenreRepository):
    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            genre_model = GenreModelMapper.to_model_orm(genre)
            genre_model.save()
            genre_model.categories.set(genre.categories)

    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre_orm = GenreORM.objects.get(id=id)
        except GenreORM.DoesNotExist:
            return None
        return GenreModelMapper.to_entity(genre_orm)

    def delete(self, id: UUID) -> None:
        GenreORM.objects.filter(id=id).delete()

    def update(self, genre: Genre) -> None:
        try:
            genre_orm = GenreORM.objects.get(id=genre.id)
        except GenreORM.DoesNotExist:
            return

        with transaction.atomic():
            GenreORM.objects.filter(id=genre.id).update(name=genre.name, is_active=genre.is_active)
            genre_orm.categories.set(genre.categories)

    def list(self) -> List[Genre]:
        return [
            GenreModelMapper.to_entity(genre_model)
            for genre_model in GenreORM.objects.all()
        ]


class GenreModelMapper:
    @staticmethod
    def to_entity(genre: GenreORM) -> Genre:
        return Genre(id=genre.id, name=genre.name, is_active=genre.is_active,
                     categories={cat.id for cat in genre.categories.all()})

    @staticmethod
    def to_model_orm(genre: Genre) -> GenreORM:
        return GenreORM(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
        )

