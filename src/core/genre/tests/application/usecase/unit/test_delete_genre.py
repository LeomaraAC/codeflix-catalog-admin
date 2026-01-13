import uuid
from unittest.mock import create_autospec
import pytest

from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.application.usecase.delete_genre import DeleteGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class TestDeleteGenre:
    def test_delete_genre_from_repository(self):
        mock_genre = Genre(name='Action', categories={uuid.uuid4()})
        mock_repository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = mock_genre

        use_case = DeleteGenre(repository=mock_repository)
        use_case.execute(request=DeleteGenre.Input(id=mock_genre.id))
        mock_repository.delete.assert_called_once_with(mock_genre.id)


    def test_when_genre_not_found_then_raise_exception(self):
        mock_repository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = None

        not_found_genre_id = uuid.uuid4()

        use_case = DeleteGenre(repository=mock_repository)
        with pytest.raises(GenreNotFound, match=f'Genre with id {not_found_genre_id} not found'):
            use_case.execute(request=DeleteGenre.Input(id=not_found_genre_id))

        mock_repository.delete.assert_not_called()
