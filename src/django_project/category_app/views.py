from uuid import UUID

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
    HTTP_204_NO_CONTENT

from src.core.category.application.usecase.create_category import CreateCategoryRequest, CreateCategory
from src.core.category.application.usecase.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.usecase.exceptions import CategoryNotFound
from src.core.category.application.usecase.get_category import GetCategory, GetCategoryRequest
from src.core.category.application.usecase.list_category import ListCategoryRequest, ListCategory
from src.core.category.application.usecase.update_category import UpdateCategoryRequest, UpdateCategory
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.category_app.serializers import ListCategoryResponseSerializer, \
    RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer, CreateCategoryRequestSerializer, \
    CreateCategoryResponseSerializer, UpdateCategoryRequestSerializer, DeleteCategoryRequestSerializer


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        response = use_case.execute(request=ListCategoryRequest())

        serializer = ListCategoryResponseSerializer(instance=response)

        return Response(status=HTTP_200_OK, data=serializer.data)

    def retrieve(self, request: Request, pk=None) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={'id': pk})
        serializer.is_valid(raise_exception=True)

        use_case = GetCategory(repository=DjangoORMCategoryRepository())
        try:
            response = use_case.execute(request=GetCategoryRequest(id=serializer.validated_data['id']))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category_data = RetrieveCategoryResponseSerializer(instance=response)
        return Response(status=HTTP_200_OK, data=category_data.data)

    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCategoryRequest(**serializer.validated_data)
        use_case = CreateCategory(repository=DjangoORMCategoryRepository())
        response = use_case.execute(request=input)

        return Response(status=HTTP_201_CREATED, data=CreateCategoryResponseSerializer(instance=response).data)

    def update(self, request: Request, pk=None) -> Response:
        serializer = UpdateCategoryRequestSerializer(data={**request.data, 'id': pk})
        serializer.is_valid(raise_exception=True)

        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=UpdateCategoryRequest(**serializer.validated_data))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk=None) -> Response:
        serializer = DeleteCategoryRequestSerializer(data={'id': pk})
        serializer.is_valid(raise_exception=True)
        use_case = DeleteCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=DeleteCategoryRequest(**serializer.validated_data))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def partial_update(self, request: Request, pk=None) -> Response:
        serializer = UpdateCategoryRequestSerializer(data={**request.data, 'id': pk}, partial=True)
        serializer.is_valid(raise_exception=True)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=UpdateCategoryRequest(**serializer.validated_data))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)
