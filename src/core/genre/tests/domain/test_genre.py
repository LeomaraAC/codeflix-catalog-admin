import pytest
import uuid
from uuid import UUID

from src.core.genre.domain.genre import Genre


class TestGenre:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match='missing 1 required positional argument: \'name\''):
            Genre()

    def test_name_must_have_less_than_255_characters(self):
        long_name = 'a' * 256
        with pytest.raises(ValueError, match='name cannot be longer than 255 characters'):
            Genre(name=long_name)

    def test_cannot_create_genre_with_empty_name(self):
        with pytest.raises(ValueError, match='name cannot be empty'):
            Genre(name='')

    def test_genre_must_be_created_with_id_as_uuid4(self):
        genre = Genre(name='Comedy')

        assert genre.id is not None
        assert isinstance(genre.id, UUID)

    def test_created_genre_with_default_values(self):
        genre = Genre(name='Fantasy')

        assert genre.name == 'Fantasy'
        assert genre.is_active is True
        assert genre.categories == set()

    def test_genre_is_created_with_provided_values(self):
        genre_id = uuid.uuid4()
        categories = {uuid.uuid4(), uuid.uuid4()}
        genre = Genre(name='Adventure', id=genre_id, is_active=False, categories=categories)

        assert genre.name == 'Adventure'
        assert genre.id == genre_id
        assert genre.is_active is False
        assert genre.categories == categories

    def test_genre_str_representation(self):
        genre = Genre(name='Thriller', is_active=True)

        assert str(genre) == 'Thriller (Active: True)'

    def test_genre_repr_representation(self):
        cat_id = uuid.uuid4()

        genre = Genre(name='Action', id=cat_id)

        assert repr(genre) == f'<Genre id={cat_id} name=Action>'


class TestChangeNameGenre:
    def test_update_genre_name(self):
        new_name = 'Horror'

        genre = Genre(name='Thriller')

        genre.change_name(name=new_name)

        assert genre.name == new_name

    def test_update_genre_with_empty_name(self):
        genre = Genre(name='Drama')

        with pytest.raises(ValueError, match='name cannot be empty'):
            genre.change_name(name='')

    def test_update_genre_with_long_name(self):
        long_name = 'a' * 256
        genre = Genre(name='Animation')

        with pytest.raises(ValueError, match='name cannot be longer than 255 characters'):
            genre.change_name(name=long_name)

class TestAddCategoryToGenre:
    def test_add_category_to_genre(self):
        category_id = uuid.uuid4()
        genre = Genre(name='Documentary')

        assert category_id not in genre.categories
        genre.add_category(category_id)

        assert category_id in genre.categories

    def test_add_existing_category_to_genre(self):
        category_id = uuid.uuid4()
        genre = Genre(name='Documentary', categories={category_id})

        assert category_id in genre.categories
        genre.add_category(category_id)
        assert len(genre.categories) == 1
        assert category_id in genre.categories

    def test_add_more_than_one_category_to_genre(self):
        category_id1 = uuid.uuid4()
        category_id2 = uuid.uuid4()
        genre = Genre(name='Documentary')

        assert category_id1 not in genre.categories
        assert category_id2 not in genre.categories

        genre.add_category(category_id1)
        genre.add_category(category_id2)

        assert category_id1 in genre.categories
        assert category_id2 in genre.categories
        assert len(genre.categories) == 2

class TestRemoveCategoryFromGenre:
    def test_remove_existing_category_from_genre(self):
        category_id = uuid.uuid4()
        genre = Genre(name='Documentary', categories={category_id})

        assert category_id in genre.categories
        genre.remove_category(category_id)

        assert category_id not in genre.categories

    def test_remove_non_existing_category_from_genre(self):
        category_id = uuid.uuid4()
        genre = Genre(name='Documentary')

        assert category_id not in genre.categories
        genre.remove_category(category_id)

        assert category_id not in genre.categories



class TestDeactivateGenre:
    def test_deactivate_active_genre(self):
        genre = Genre(name='Romance', is_active=True)

        genre.deactivate()

        assert genre.is_active is False

    def test_deactivate_already_inactive_genre(self):
        genre = Genre(name='Sci-Fi', is_active=False)

        genre.deactivate()

        assert genre.is_active is False


class TestActivateGenre:

    def test_activate_inactive_genre(self):
        genre = Genre(name='Romance', is_active=False)

        genre.activate()

        assert genre.is_active is True

    def test_activate_already_active_genre(self):
        genre = Genre(name='Romance', is_active=True)

        genre.activate()

        assert genre.is_active is True


class TestEquality:
    def test_categories_with_same_id_are_equal(self):
        cat_id = uuid.uuid4()
        genre1 = Genre(name='Thriller', id=cat_id)
        genre2 = Genre(name='Horror', id=cat_id)

        assert genre1 == genre2

    def test_categories_with_different_ids_are_not_equal(self):
        genre1 = Genre(name='Thriller', id=uuid.uuid4())
        genre2 = Genre(name='Horror', id=uuid.uuid4())

        assert genre1 != genre2

    def test_genre_not_equal_to_different_type(self):
        class Dummy:
            pass

        cat_id = uuid.uuid4()
        genre = Genre(name='Comedy', id=cat_id)
        dummy = Dummy()
        dummy.id = cat_id

        assert genre != dummy
