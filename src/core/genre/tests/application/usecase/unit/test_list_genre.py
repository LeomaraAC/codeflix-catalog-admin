from unittest.mock import create_autospec
from uuid import uuid4

from src.core.genre.application.usecase.list_genre import ListGenre, GenreOutput
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class TestListGenre:
    def test_list_genre_with_associated_categories(self):
        genre_repository = create_autospec(GenreRepository)
        genre_drama = Genre(name='Drama',categories={uuid4()})
        genre_romance = Genre(name='Romance')
        genre_repository.list.return_value = [genre_drama, genre_romance]

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())


        genre_repository.list.assert_called_once()
        assert len(output.data) == 2
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre_drama.id,
                    name=genre_drama.name,
                    categories=genre_drama.categories,
                    is_active=genre_drama.is_active,
                ),
                GenreOutput(
                    id=genre_romance.id,
                    name=genre_romance.name,
                    categories=set(),
                    is_active=genre_romance.is_active,
                ),
            ]
        )

    def test_list_genre_empty_repository(self):
        genre_repository = create_autospec(GenreRepository)
        genre_repository.list.return_value = []

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        genre_repository.list.assert_called_once()
        assert len(output.data) == 0
        assert output == ListGenre.Output(data=[])
