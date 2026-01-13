from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre_repository import GenreRepository


class UpdateGenre:
    def __init__(self, genre_repository: GenreRepository, category_repository: CategoryRepository):
        self.genre_repository = genre_repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        id: UUID
        name: str | None = None
        is_active: bool | None = None
        category_ids: set[UUID] | None = None

    def execute(self, input: Input) -> None:
        genre = self.genre_repository.get_by_id(input.id)
        if not genre:
            raise GenreNotFound(f'Genre with ID {input.id} not found')

        name = input.name if input.name is not None else genre.name
        categories = input.category_ids if input.category_ids is not None else genre.categories
        category_ids = {category.id for category in self.category_repository.list()}
        if not categories.issubset(category_ids):
            raise RelatedCategoriesNotFound(f'Categories not found: {str(input.category_ids - category_ids)}')

        try:
            genre.change_name(name)
            categories_to_remove = genre.categories - categories
            for category_id in categories_to_remove:
                genre.remove_category(category_id)

            categories_to_add = categories - genre.categories
            for category_id in categories_to_add:
                genre.add_category(category_id)
        except ValueError as e:
            raise InvalidGenre(e)

        if input.is_active:
            genre.activate()

        if input.is_active is False:
            genre.deactivate()

        self.genre_repository.update(genre)
