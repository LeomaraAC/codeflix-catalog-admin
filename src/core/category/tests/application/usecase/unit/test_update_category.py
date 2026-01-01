import uuid
from unittest.mock import create_autospec

import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.usecase.exceptions import CategoryNotFound, InvalidCategoryData
from src.core.category.application.usecase.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(name='Films', description='Category for films')
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        usecase = UpdateCategory(repository=mock_repository)
        usecase.execute(request=UpdateCategoryRequest(id=category.id, name='Series'))

        mock_repository.get_by_id.assert_called_once_with(id=category.id)
        mock_repository.update.assert_called_once()
        assert category.name == 'Series'
        assert category.description == 'Category for films'

    def test_update_category_description(self):
        category = Category(name='Series', description='Category for series')
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        usecase = UpdateCategory(repository=mock_repository)
        usecase.execute(request=UpdateCategoryRequest(id=category.id, description='Category for TV series'))

        mock_repository.get_by_id.assert_called_once_with(id=category.id)
        mock_repository.update.assert_called_once()
        assert category.name == 'Series'
        assert category.description == 'Category for TV series'

    def test_update_category_name_and_description(self):
        category = Category(name='Series', description='Category for series')
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        usecase = UpdateCategory(repository=mock_repository)
        usecase.execute(request=UpdateCategoryRequest(id=category.id, name='TV Series', description='Category for TV series'))

        mock_repository.get_by_id.assert_called_once_with(id=category.id)
        mock_repository.update.assert_called_once()
        assert category.name == 'TV Series'
        assert category.description == 'Category for TV series'

    def test_can_deactivate_category(self):
        category = Category(name='Films', description='Category for films', is_active=True)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        usecase = UpdateCategory(repository=mock_repository)
        usecase.execute(request=UpdateCategoryRequest(id=category.id, is_active=False))

        mock_repository.get_by_id.assert_called_once_with(id=category.id)
        mock_repository.update.assert_called_once_with(category)
        assert category.is_active is False
        assert category.description == 'Category for films'
        assert category.name == 'Films'

    def test_can_activate_category(self):
        category = Category(name='Films', description='Category for films', is_active=False)
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        usecase = UpdateCategory(repository=mock_repository)
        usecase.execute(request=UpdateCategoryRequest(id=category.id, is_active=True))

        mock_repository.get_by_id.assert_called_once_with(id=category.id)
        mock_repository.update.assert_called_once_with(category)
        assert category.is_active is True
        assert category.description == 'Category for films'
        assert category.name == 'Films'

    def test_when_category_does_not_exist_then_return_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateCategory(repository=mock_repository)
        not_found_id = uuid.uuid4()
        with pytest.raises(CategoryNotFound, match=f'Category with id {not_found_id} not found'):
            use_case.execute(request=UpdateCategoryRequest(id=not_found_id))

        mock_repository.get_by_id.assert_called_once()
        mock_repository.update.assert_not_called()

    def test_when_name_is_invalid_then_raise_exception(self):
        category = Category(name='Films', description='Category for films')
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        with pytest.raises(InvalidCategoryData):
            use_case.execute(request=UpdateCategoryRequest(id=category.id, name='a'*256))

        mock_repository.get_by_id.assert_called_once_with(id=category.id)
        mock_repository.update.assert_not_called()
