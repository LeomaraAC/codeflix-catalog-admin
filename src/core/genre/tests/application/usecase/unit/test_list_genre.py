from unittest.mock import create_autospec
from uuid import uuid4

from src.core._shared.application.list_response import ListResponse, ListOutputMeta
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
        assert output == ListResponse(
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
            ],
            meta=ListOutputMeta(current_page=1, per_page=2, total=2)
        )

    def test_list_genre_ordered_by_name_with_pagination(self):
        genre_repository = create_autospec(GenreRepository)
        genre_romance = Genre(name='Romance')
        genre_action = Genre(name='Action')
        genre_drama = Genre(name='Drama')
        genre_repository.list.return_value = [genre_romance, genre_action, genre_drama]

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input(order_by='name', current_page=2))

        assert len(output.data) == 1
        assert output.data[0].name == 'Romance'
        assert output.meta == ListOutputMeta(current_page=2, per_page=2, total=3)

    def test_list_genre_empty_repository(self):
        genre_repository = create_autospec(GenreRepository)
        genre_repository.list.return_value = []

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        genre_repository.list.assert_called_once()
        assert len(output.data) == 0
        assert output == ListResponse(data=[], meta=ListOutputMeta(current_page=1, per_page=2, total=0))
