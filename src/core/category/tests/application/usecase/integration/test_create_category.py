from uuid import UUID

from src.core.category.application.usecase.create_category import CreateCategory, CreateCategoryRequest, CreateCategoryResponse
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestCreateCategory:
    def test_create_category_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(name='Films',  description='Category for films')
        response = use_case.execute(request)
        persisted_category = repository.categories[0]

        assert response is not None
        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1
        assert persisted_category.id == response.id
        assert persisted_category.name == 'Films'
        assert persisted_category.description == 'Category for films'
        assert persisted_category.is_active == True

    def test_create_inactive_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryRequest(name='Series', description='Category for series', is_active=False)
        response = use_case.execute(request)
        persisted_category = repository.categories[0]

        assert response is not None
        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1
        assert persisted_category.id == response.id
        assert persisted_category.name == 'Series'
        assert persisted_category.description == 'Category for series'
        assert persisted_category.is_active == False

