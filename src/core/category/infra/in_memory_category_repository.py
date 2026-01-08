from typing import List, Optional
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.domain.category import Category


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories: List[Category] = None):
        self.categories = categories or []

    def save(self, category):
        self.categories.append(category)

    def get_by_id(self, id: UUID) -> Optional[Category]:
        return next((category for category in self.categories if category.id == id), None)

    def delete(self, id: UUID) -> None:
        category = self.get_by_id(id)
        if not category:
            return
        self.categories.remove(category)
        # self.categories = [category for category in self.categories if category.id != id]

    def update(self, category: Category) -> None:
        if not category in self.categories:
            return
        index = self.categories.index(category)
        self.categories[index] = category

    def list(self) -> List[Category]:
        return [category for category in self.categories]
