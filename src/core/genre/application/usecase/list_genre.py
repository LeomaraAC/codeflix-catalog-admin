from dataclasses import dataclass
from typing import List
from uuid import UUID

from src.core._shared.application.list_response import ListResponse, ListOutputMeta
from src.core._shared.application.list_utils import ListUtils
from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]


class ListGenre:
    def __init__(self, repository: GenreRepository):
        self.repository = repository

    @dataclass
    class Input:
        order_by: str = 'name'
        current_page: int = 1

    def execute(self, input: Input) -> ListResponse[GenreOutput]:
        genres = self.repository.list()
        sorted_genres = ListUtils.sort([
            GenreOutput(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=genre.categories
            ) for genre in genres
        ], order_by=input.order_by)

        genre_page = ListUtils.paginate(sorted_genres, current_page=input.current_page)

        return ListResponse[GenreOutput](data=genre_page, meta=ListOutputMeta(current_page=input.current_page,
                                                                              per_page=ListUtils.DEFAULT_PAGE_SIZE,
                                                                              total=len(sorted_genres)))
