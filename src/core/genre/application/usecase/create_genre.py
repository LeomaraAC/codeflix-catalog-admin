from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import RelatedCategoriesNotFound, InvalidGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class CreateGenre:
    def __init__(self, repository: GenreRepository, category_repository: CategoryRepository):
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        name: str
        category_ids: set[UUID] = field(default_factory=set)
        is_active: bool = True

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        category_ids = {category.id for category in self.category_repository.list()}
        if not input.category_ids.issubset(category_ids):
            raise RelatedCategoriesNotFound(f'Categories not found: {str(input.category_ids - category_ids)}')

        try:
            genre = Genre(name=input.name, categories=input.category_ids, is_active=input.is_active)
        except ValueError as e:
            raise InvalidGenre(e)

        self.repository.save(genre)

        return self.Output(id=genre.id)