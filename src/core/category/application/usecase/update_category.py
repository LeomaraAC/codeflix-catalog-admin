from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.usecase.exceptions import CategoryNotFound, InvalidCategoryData


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: UpdateCategoryRequest) -> None:
        category = self.repository.get_by_id(request.id)
        if not category:
            raise CategoryNotFound(f'Category with id {request.id} not found')

        name = request.name if request.name is not None else category.name
        description = request.description if request.description is not None else category.description

        try:
            category.update_category(name=name, description=description)
        except ValueError as e:
            raise InvalidCategoryData(e)

        if request.is_active:
            category.activate()

        if request.is_active is False:
            category.deactivate()

        self.repository.update(category)
