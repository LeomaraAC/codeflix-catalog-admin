import uuid

import pytest

from src.core.genre.domain.genre import Genre
from src.django_project.genre_app.models import Genre as GenreORM
from src.core.category.domain.category import Category
from src.django_project.category_app.models import Category as CategoryORM
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.mark.django_db
class TestSave:
    def test_save_genre_in_database(self):
        genre = Genre(name='Action')
        genre_repository = DjangoORMGenreRepository()

        assert GenreORM.objects.count() == 0

        genre_repository.save(genre)

        assert GenreORM.objects.count() == 1
        genre_orm = GenreORM.objects.first()
        assert genre_orm is not None
        assert genre_orm.id == genre.id
        assert genre_orm.name == genre.name
        assert genre_orm.is_active == genre.is_active

    def test_save_genre_with_categories_in_database(self):
        genre_repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category = Category(name='Documentary')
        category_repository.save(category)

        genre = Genre(name='Action')
        genre.add_category(category.id)

        assert GenreORM.objects.count() == 0

        genre_repository.save(genre)

        assert GenreORM.objects.count() == 1
        genre_orm = GenreORM.objects.get(id=genre.id)
        related_categories = genre_orm.categories.get()

        assert genre_orm is not None
        assert genre_orm.id == genre.id
        assert genre_orm.name == genre.name
        assert genre_orm.is_active == genre.is_active
        assert related_categories.id == category.id


@pytest.mark.django_db
class TestGetById:
    def test_get_genre_by_id_from_database(self):
        category = CategoryORM.objects.create(name='Film')

        genre_orm = GenreORM.objects.create(
            name='Horror',
            is_active=True
        )
        genre_orm.categories.add(category)

        genre_repository = DjangoORMGenreRepository()

        genre = genre_repository.get_by_id(id=genre_orm.id)

        assert genre is not None
        assert type(genre) == Genre
        assert genre.id == genre_orm.id
        assert genre.name == genre_orm.name
        assert genre.is_active == genre_orm.is_active
        assert category.id in genre.categories

    def test_when_genre_does_not_exist_then_return_none(self):
        genre_repository = DjangoORMGenreRepository()
        not_found_id = uuid.uuid4()

        genre = genre_repository.get_by_id(id=not_found_id)

        assert genre is None

    def test_get_genre_without_categories(self):
        genre_orm = GenreORM.objects.create(
            name='Comedy',
            is_active=True
        )

        genre_repository = DjangoORMGenreRepository()

        genre = genre_repository.get_by_id(id=genre_orm.id)

        assert genre is not None
        assert type(genre) == Genre
        assert genre.id == genre_orm.id
        assert genre.name == genre_orm.name
        assert genre.is_active == genre_orm.is_active
        assert len(genre.categories) == 0

@pytest.mark.django_db
class TestDelete:
    def test_delete_genre_by_id_from_database(self):
        genre_sci_fi = GenreORM.objects.create(
            name='Sci-Fi',
            is_active=True
        )

        genre_romance = GenreORM.objects.create(
            name='Romance',
            is_active=True
        )

        genre_repository = DjangoORMGenreRepository()

        assert GenreORM.objects.count() == 2

        genre_repository.delete(id=genre_sci_fi.id)

        assert GenreORM.objects.count() == 1
        remaining_genre = GenreORM.objects.first()
        assert remaining_genre.id == genre_romance.id

    def test_when_genre_does_not_exist_then_no_effect(self):
        GenreORM.objects.create(
            name='Sci-Fi',
            is_active=True
        )
        genre_repository = DjangoORMGenreRepository()
        not_found_id = uuid.uuid4()

        assert GenreORM.objects.count() == 1

        genre_repository.delete(id=not_found_id)

        assert GenreORM.objects.count() == 1

@pytest.mark.django_db
class TestUpdate:
    def test_update_genre_in_database(self):
        category_film = CategoryORM.objects.create(name='Film')
        category_documentary = CategoryORM.objects.create(name='Documentary')

        genre_orm = GenreORM.objects.create(
            name='Action',
            is_active=True
        )
        genre_orm.categories.add(category_film)

        genre_repository = DjangoORMGenreRepository()

        genre = Genre(
            id=genre_orm.id,
            name='Action & Adventure',
            is_active=False,
            categories={category_documentary.id, category_film.id}
        )

        genre_repository.update(genre)

        updated_genre_orm = GenreORM.objects.get(id=genre_orm.id)
        related_categories = {cat.id for cat in updated_genre_orm.categories.all()}

        assert updated_genre_orm.name == 'Action & Adventure'
        assert updated_genre_orm.is_active is False
        assert len(related_categories) == 2
        assert category_documentary.id in related_categories
        assert category_film.id in related_categories

@pytest.mark.django_db
class TestList:
    def test_list_all_genres_from_database(self):
        category_film = CategoryORM.objects.create(name='Film')
        category_series = CategoryORM.objects.create(name='Series')

        genre_orm_mystery = GenreORM.objects.create(
            name='Mystery',
            is_active=True
        )
        genre_orm_mystery.categories.add(category_film)

        genre_orm_horror = GenreORM.objects.create(
            name='Horror',
            is_active=False
        )
        genre_orm_horror.categories.add(category_series)

        genre_repository = DjangoORMGenreRepository()

        genres = genre_repository.list()

        assert len(genres) == 2

        genre_mystery = next((g for g in genres if g.id == genre_orm_mystery.id), None)
        genre_horror = next((g for g in genres if g.id == genre_orm_horror.id), None)

        assert genre_mystery is not None
        assert genre_mystery.name == genre_orm_mystery.name
        assert genre_mystery.is_active == genre_orm_mystery.is_active
        assert category_film.id in genre_mystery.categories

        assert genre_horror is not None
        assert genre_horror.name == genre_orm_horror.name
        assert genre_horror.is_active == genre_orm_horror.is_active
        assert category_series.id in genre_horror.categories

    def test_list_genres_when_database_is_empty(self):
        genre_repository = DjangoORMGenreRepository()

        genres = genre_repository.list()

        assert len(genres) == 0
