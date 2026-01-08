from uuid import UUID

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from django_project.category_app.models import Category as CategoryModel


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, category_model: CategoryModel = CategoryModel) -> None:
        self.category_model = category_model

    def save(self, category: Category) -> None:
        self.category_model.objects.create(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category_record = self.category_model.objects.get(id=id)
            return Category(
                id=category_record.id,
                name=category_record.name,
                description=category_record.description,
                is_active=category_record.is_active
            )
        except self.category_model.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        self.category_model.objects.filter(id=id).delete()

    def update(self, category: Category) -> None:
        self.category_model.objects.filter(pk=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )

    def list(self) -> list[Category]:
        return [
            Category(
                id=record.id,
                name=record.name,
                description=record.description,
                is_active=record.is_active
            ) for record in self.category_model.objects.all()
        ]