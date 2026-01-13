import uuid
from unittest.mock import create_autospec
import pytest

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.usecase.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.usecase.exceptions import CategoryNotFound
from src.core.category.domain.category import Category


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        mock_category = Category(name='Films', description='Category for films')
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = mock_category

        use_case = DeleteCategory(repository=mock_repository)
        use_case.execute(request=DeleteCategoryRequest(id=mock_category.id))
        mock_repository.delete.assert_called_once_with(mock_category.id)


    def test_when_category_not_found_then_raise_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteCategory(repository=mock_repository)
        with pytest.raises(CategoryNotFound):
            use_case.execute(request=DeleteCategoryRequest(id=uuid.uuid4()))

        mock_repository.delete.assert_not_called()
