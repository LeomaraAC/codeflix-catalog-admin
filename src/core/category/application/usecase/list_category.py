from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.list_response import ListResponse, ListOutputMeta
from src.core._shared.application.list_utils import ListUtils
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


@dataclass
class ListCategoryRequest:
    order_by: str = 'name'
    current_page: int = 1


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: ListCategoryRequest) -> ListResponse[CategoryOutput]:
        categories = self.repository.list()
        sorted_categories = ListUtils.sort([
            CategoryOutput(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active
            ) for category in categories
        ], order_by=request.order_by)

        categories_page = ListUtils.paginate(sorted_categories, current_page=request.current_page)

        return ListResponse[CategoryOutput](data=categories_page,
                                            meta=ListOutputMeta(current_page=request.current_page,
                                                                per_page=ListUtils.DEFAULT_PAGE_SIZE,
                                                                total=len(sorted_categories)))
