import uuid
from unittest.mock import create_autospec
import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.usecase.exceptions import CategoryNotFound
from src.core.category.application.usecase.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category


class TestGetCategory:
    def test_when_category_exists_then_return_response_dto(self):
        mock_category = Category(name='Films', description='Category for films')
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = mock_category

        use_case = GetCategory(repository=mock_repository)
        response = use_case.execute(request=GetCategoryRequest(id=mock_category.id))

        assert response == GetCategoryResponse(id=mock_category.id, name=mock_category.name,
                                               description=mock_category.description, is_active=mock_category.is_active)

    def test_when_category_does_not_exist_then_return_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetCategory(repository=mock_repository)
        not_found_id = uuid.uuid4()
        with pytest.raises(CategoryNotFound, match=f'Category with id {not_found_id} not found'):
            use_case.execute(request=GetCategoryRequest(id=not_found_id))
