from unittest.mock import create_autospec

from src.core._shared.application.list_response import ListResponse
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.usecase.list_category import ListCategory, CategoryOutput, ListCategoryRequest, \
    ListOutputMeta
from src.core.category.domain.category import Category


class TestListCategory:
    def test_when_no_category_then_return_empty_list(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = []

        use_case = ListCategory(repository=mock_repository)
        response = use_case.execute(request=ListCategoryRequest())

        assert response == ListResponse(data=[], meta=ListOutputMeta(current_page=1, per_page=2, total=0))

    def test_when_category_exists_then_return__mapped_list(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series', is_active=False)

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = [category_film, category_series]

        use_case = ListCategory(repository=mock_repository)
        response = use_case.execute(request=ListCategoryRequest())

        assert len(response.data) == 2
        assert response == ListResponse(data=[
            CategoryOutput(id=category_film.id, name=category_film.name,
                           description=category_film.description, is_active=category_film.is_active),
            CategoryOutput(id=category_series.id, name=category_series.name,
                           description=category_series.description, is_active=category_series.is_active),
        ], meta=ListOutputMeta(current_page=1, per_page=2, total=2))

    def test_when_order_by_description_then_return_ordered_list(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='About series', is_active=False)

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = [category_film, category_series]

        use_case = ListCategory(repository=mock_repository)
        response = use_case.execute(request=ListCategoryRequest(order_by='description'))

        assert len(response.data) == 2
        assert response == ListResponse(data=[
            CategoryOutput(id=category_series.id, name=category_series.name,
                           description=category_series.description, is_active=category_series.is_active),
            CategoryOutput(id=category_film.id, name=category_film.name,
                           description=category_film.description, is_active=category_film.is_active),
        ], meta=ListOutputMeta(current_page=1, per_page=2, total=2))

    def test_when_order_by_description_with_none_then_none_last(self):
        category_with_desc = Category(name='Films', description='A description')
        category_no_desc = Category(name='Series', description=None)

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = [category_no_desc, category_with_desc]

        use_case = ListCategory(repository=mock_repository)
        response = use_case.execute(request=ListCategoryRequest(order_by='description'))

        assert len(response.data) == 2
        assert response.data[0].description == 'A description'
        assert response.data[1].description is None

    def test_with_paginated_list(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='About series', is_active=False)
        animation_series = Category(name='Animation', description='Category for Animations', is_active=False)

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = [category_film, category_series, animation_series]

        use_case = ListCategory(repository=mock_repository)
        response = use_case.execute(request=ListCategoryRequest(current_page=2))

        assert len(response.data) == 1
        assert response == ListResponse(data=[
            CategoryOutput(id=category_series.id, name=category_series.name,
                           description=category_series.description, is_active=category_series.is_active)
        ], meta=ListOutputMeta(current_page=2, per_page=2, total=3))
