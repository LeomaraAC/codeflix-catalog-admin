from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.usecase.exceptions import CategoryNotFound


@dataclass
class DeleteCategoryRequest:
    id: UUID


class DeleteCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: DeleteCategoryRequest) -> None:
        category = self.repository.get_by_id(request.id)
        if not category:
            raise CategoryNotFound(f'Category with id {request.id} not found')

        self.repository.delete(id = request.id)
