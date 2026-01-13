import uuid

import pytest

from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.application.usecase.delete_genre import DeleteGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def genre_action() -> Genre:
    return Genre(name='Action')


@pytest.fixture
def genre_drama() -> Genre:
    return Genre(name='Drama', is_active=False)


@pytest.fixture
def repository(genre_action: Genre, genre_drama) -> InMemoryGenreRepository:
    return InMemoryGenreRepository(genres=[genre_action, genre_drama])


class TestDeleteGenre:
    def test_get_genre_by_id(self, genre_action: Genre, genre_drama: Genre, repository: InMemoryGenreRepository):
        use_case = DeleteGenre(repository=repository)

        assert repository.get_by_id(genre_action.id) is not None
        assert repository.get_by_id(genre_drama.id) is not None

        use_case.execute(request=DeleteGenre.Input(id=genre_action.id))

        assert repository.get_by_id(genre_action.id) is None
        assert repository.get_by_id(genre_drama.id) is not None

    def test_when_genre_does_not_exist_then_raise_exception(self, genre_action: Genre, genre_drama: Genre,
                                                            repository: InMemoryGenreRepository):
        use_case = DeleteGenre(repository=repository)
        with pytest.raises(GenreNotFound, match='Genre with id .* not found'):
            use_case.execute(request=DeleteGenre.Input(id=uuid.uuid4()))

        assert len(repository.genres) == 2
        assert repository.get_by_id(genre_action.id) is not None
        assert repository.get_by_id(genre_drama.id) is not None
