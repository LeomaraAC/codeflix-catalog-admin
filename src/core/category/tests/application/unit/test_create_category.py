from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.create_category import CreateCategory, CreateCategoryRequest, CreateCategoryResponse
from src.core.category.application.exceptions import InvalidCategoryData


class TestCreateCategory:
    def test_create_category_valid_data(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(name='Films',  description='Category for films', is_active=True)
        category_response = use_case.execute(request)

        assert category_response is not None
        assert isinstance(category_response, CreateCategoryResponse)
        assert isinstance(category_response.id, UUID)
        assert mock_repository.save.call_count == 1
        assert mock_repository.save.called is True

    def test_create_category_invalid_data(self):
        use_case = CreateCategory(repository=MagicMock(CategoryRepository))
        with pytest.raises(InvalidCategoryData, match='name cannot be empty'):
            use_case.execute(request=CreateCategoryRequest(name=''))