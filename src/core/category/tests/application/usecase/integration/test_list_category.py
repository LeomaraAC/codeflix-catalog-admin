from src.core.category.application.usecase.list_category import ListCategory, ListCategoryResponse, CategoryOutput, \
    ListCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestListCategory:
    def test_when_no_category_then_return_empty_list(self):
        repository = InMemoryCategoryRepository(categories=[])

        use_case = ListCategory(repository=repository)
        response = use_case.execute(request=ListCategoryRequest())

        assert response == ListCategoryResponse(data=[])

    def test_when_category_exists_then_return__mapped_list(self):
        category_film = Category(name='Films', description='Category for films')
        category_series = Category(name='Series', description='Category for series', is_active=False)

        repository = InMemoryCategoryRepository(categories=[category_film, category_series])

        use_case = ListCategory(repository=repository)
        response = use_case.execute(request=ListCategoryRequest())


        assert len(response.data) == 2
        assert response == ListCategoryResponse(data=[
            CategoryOutput(id=category_film.id, name=category_film.name,
                           description=category_film.description, is_active=category_film.is_active),
            CategoryOutput(id=category_series.id, name=category_series.name,
                           description=category_series.description, is_active=category_series.is_active),
        ])

