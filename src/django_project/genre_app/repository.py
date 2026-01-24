from typing import List
from uuid import UUID

from django.db import transaction

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import Genre as GenreORM


class DjangoORMGenreRepository(GenreRepository):
    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            genre_model = GenreORM.objects.create(id=genre.id, name=genre.name, is_active=genre.is_active)
            genre_model.categories.set(genre.categories)

    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre_orm = GenreORM.objects.get(id=id)
        except GenreORM.DoesNotExist:
            return None
        return Genre(id=genre_orm.id, name=genre_orm.name, is_active=genre_orm.is_active,
                     categories={cat.id for cat in genre_orm.categories.all()})

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
            Genre(id=genre_model.id,
                  name=genre_model.name,
                  is_active=genre_model.is_active,
                  categories={cat.id for cat in genre_model.categories.all()})
            for genre_model in GenreORM.objects.all()
        ]
