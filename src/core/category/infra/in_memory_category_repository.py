from typing import List, Optional
from uuid import UUID

from src.core.category.application.category_repository import CategoryRepository
from src.core.category.domain.category import Category


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories: List[Category] = None):
        self.categories = categories or []

    def save(self, category):
        self.categories.append(category)

    def get_by_id(self, id: UUID) -> Optional[Category]:
        return next((category for category in self.categories if category.id == id), None)
