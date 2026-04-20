from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, \
    HTTP_204_NO_CONTENT

from src.core._shared.application.list_response import ListResponse
from src.core.cast_member.application.exceptions import InvalidCastMember, CastMemberNotFound
from src.core.cast_member.application.usecase.create_cast_member import CreateCastMember
from src.core.cast_member.application.usecase.delete_cast_member import DeleteCastMember
from src.core.cast_member.application.usecase.list_cast_member import ListCastMember
from src.core.cast_member.application.usecase.update_cast_member import UpdateCastMember
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.cast_member_app.serializers import CreateCastMemberInputSerializer, \
    CreateCastMemberOutputSerializer, ListCastMemberOutputSerializer, UpdateCastMemberInputSerializer, \
    DeleteCastMemberInputSerializer


class CastMemberViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCastMember.Input(**serializer.validated_data)
        usecase = CreateCastMember(repository=DjangoORMCastMemberRepository())

        try:
            output: CreateCastMember.Output = usecase.execute(input)
        except InvalidCastMember as err:
            return Response(status=HTTP_400_BAD_REQUEST, data={'error': str(err)})

        return Response(status=HTTP_201_CREATED, data=CreateCastMemberOutputSerializer(output).data)

    def list(self, request: Request) -> Response:
        order_by = request.query_params.get('order_by', 'name')
        current_page = int(request.query_params.get('current_page', 1))
        usecase = ListCastMember(repository=DjangoORMCastMemberRepository())
        output: ListResponse = usecase.execute(ListCastMember.Input(order_by=order_by, current_page=current_page))

        return Response(status=HTTP_200_OK, data=ListCastMemberOutputSerializer(instance=output).data)

    def update(self, request: Request, pk: int) -> Response:
        serializer = UpdateCastMemberInputSerializer(data={**request.data, 'id': pk})
        serializer.is_valid(raise_exception=True)

        input = UpdateCastMember.Input(**serializer.validated_data)
        usecase = UpdateCastMember(repository=DjangoORMCastMemberRepository())
        try:
            usecase.execute(input)
        except InvalidCastMember as err:
            return Response(status=HTTP_400_BAD_REQUEST, data={'error': str(err)})
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk: int) -> Response:
        serializer = DeleteCastMemberInputSerializer(data={'id': pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteCastMember.Input(**serializer.validated_data)
        usecase = DeleteCastMember(repository=DjangoORMCastMemberRepository())
        try:
            usecase.execute(input)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_204_NO_CONTENT)

