from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from src.core._shared.application.list_response import ListResponse
from src.core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound, GenreNotFound
from src.core.genre.application.usecase.create_genre import CreateGenre
from src.core.genre.application.usecase.delete_genre import DeleteGenre
from src.core.genre.application.usecase.list_genre import ListGenre
from src.core.genre.application.usecase.update_genre import UpdateGenre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import ListGenreOutputSerializer, CreateGenreInputSerializer, \
    CreateGenreOutputSerializer, DeleteGenreInputSerializer, UpdateGenreInputSerializer


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get('order_by', 'name')
        current_page = int(request.query_params.get('current_page', 1))
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListResponse = use_case.execute(input=ListGenre.Input(order_by=order_by, current_page=current_page))

        response_serializer = ListGenreOutputSerializer(instance=output)

        return Response(status=HTTP_200_OK, data=response_serializer.data)

    def create(self, request: Request) -> Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateGenre.Input(**serializer.validated_data)
        use_case = CreateGenre(repository=DjangoORMGenreRepository(), category_repository=DjangoORMCategoryRepository())
        try:
            output: CreateGenre.Output = use_case.execute(input=input)
        except (InvalidGenre, RelatedCategoriesNotFound) as err:
            return Response(status=HTTP_400_BAD_REQUEST, data={'error': str(err)})

        return Response(status=HTTP_201_CREATED, data=CreateGenreOutputSerializer(output).data)

    def update(self, request: Request, pk=None) -> Response:
        serializer = UpdateGenreInputSerializer(data={**request.data, 'id': pk})
        serializer.is_valid(raise_exception=True)

        input = UpdateGenre.Input(**serializer.validated_data)
        use_case = UpdateGenre(genre_repository=DjangoORMGenreRepository(), category_repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(input=input)
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        except (InvalidGenre, RelatedCategoriesNotFound) as err:
            return Response(status=HTTP_400_BAD_REQUEST, data={'error': str(err)})
        return Response(status=HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk=None) -> Response:
        request_data = DeleteGenreInputSerializer(data={'id': pk})
        request_data.is_valid(raise_exception=True)

        input = DeleteGenre.Input(**request_data.validated_data)
        use_case = DeleteGenre(repository=DjangoORMGenreRepository())
        try:
            use_case.execute(request=input)
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_204_NO_CONTENT)
