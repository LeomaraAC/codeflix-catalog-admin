from dataclasses import dataclass
from typing import List
from uuid import UUID

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.application.usecase.exceptions import CategoryNotFound


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool

@dataclass
class ListCategoryResponse:
    data: List[CategoryOutput]


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self) -> ListCategoryResponse:
        categories = self.repository.list()

        return ListCategoryResponse(data=[
            CategoryOutput(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active
            ) for category in categories
        ])
