from typing import List, Optional
from uuid import UUID

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class InMemoryGenreRepository(GenreRepository):
    def __init__(self, genres: List[Genre] = None):
        self.genres = genres or []

    def save(self, genre):
        self.genres.append(genre)

    def get_by_id(self, id: UUID) -> Optional[Genre]:
        return next((genre for genre in self.genres if genre.id == id), None)

    def delete(self, id: UUID) -> None:
        genre = self.get_by_id(id)
        if not genre:
            return
        self.genres.remove(genre)

    def update(self, genre: Genre) -> None:
        if not genre in self.genres:
            return
        index = self.genres.index(genre)
        self.genres[index] = genre

    def list(self) -> List[Genre]:
        return [genre for genre in self.genres]
