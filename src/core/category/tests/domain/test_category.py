import pytest
import uuid
from uuid import UUID

from src.core.category.domain.category import Category


class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match='missing 1 required positional argument: \'name\''):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        long_name = 'a' * 256
        with pytest.raises(ValueError, match='name cannot be longer than 255 characters'):
            Category(name=long_name)

    def test_category_must_be_created_with_id_as_uuid4(self):
        category = Category(name='Movies')

        assert category.id is not None
        assert isinstance(category.id, UUID)

    def test_created_category_with_default_values(self):
        category = Category(name='Movies')

        assert category.name == 'Movies'
        assert category.description == ''
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self):
        category = Category(name='Movies')

        assert category.is_active is True

    def test_category_is_created_with_provided_values(self):
        cat_id = uuid.uuid4()
        category = Category(name='Movies', id=cat_id, description='Category for movies', is_active=False)

        assert category.name == 'Movies'
        assert category.id == cat_id
        assert category.description == 'Category for movies'
        assert category.is_active is False

    def test_category_str_representation(self):
        category = Category(name='Movies', description='Category for movies', is_active=True)

        assert str(category) == 'Movies - Category for movies (Active: True)'

    def test_category_repr_representation(self):
        cat_id = uuid.uuid4()

        category = Category(name='Movies', id=cat_id)

        assert repr(category) == f'<Category id={cat_id} name=Movies>'
    
    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match='name cannot be empty'):
            Category(name='')

class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        new_name = 'Films'
        new_description = 'Category for films'

        category = Category(name='Movies', description='Category for movies')

        category.update_category(name=new_name, description=new_description)

        assert category.name == new_name
        assert category.description == new_description

    def test_update_category_with_empty_name(self):
        category = Category(name='Movies', description='Category for movies')

        with pytest.raises(ValueError, match='name cannot be empty'):
            category.update_category(name='', description='No name category')

    def test_update_category_with_long_name(self):
        long_name = 'a' * 256
        category = Category(name='Movies', description='Category for movies')

        with pytest.raises(ValueError, match='name cannot be longer than 255 characters'):
            category.update_category(name=long_name, description='Long name category')

class TestDeactivateCategory:
    def test_deactivate_active_category(self):
        category = Category(name='Movies', is_active=True)

        category.deactivate()

        assert category.is_active is False

    def test_deactivate_already_inactive_category(self):
        category = Category(name='Movies', is_active=False)

        category.deactivate()

        assert category.is_active is False

class TestActivateCategory:

    def test_activate_inactive_category(self):
        category = Category(name='Movies', is_active=False)

        category.activate()

        assert category.is_active is True
    
    def test_activate_already_active_category(self):
        category = Category(name='Movies', is_active=True)

        category.activate()

        assert category.is_active is True

class TestEquality:
    def test_categories_with_same_id_are_equal(self):
        cat_id = uuid.uuid4()
        category1 = Category(name='Movies', id=cat_id)
        category2 = Category(name='Films', id=cat_id)

        assert category1 == category2

    def test_categories_with_different_ids_are_not_equal(self):
        category1 = Category(name='Movies', id=uuid.uuid4())
        category2 = Category(name='Films', id=uuid.uuid4())

        assert category1 != category2
    
    def test_category_not_equal_to_different_type(self):
        class Dummy:
            pass

        cat_id = uuid.uuid4()
        category = Category(name='Movies', id=cat_id)
        dummy = Dummy()
        dummy.id = cat_id

        assert category != dummy