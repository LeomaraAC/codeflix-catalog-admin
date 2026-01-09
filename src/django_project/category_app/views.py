from uuid import UUID

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.core.category.application.usecase.exceptions import CategoryNotFound
from src.core.category.application.usecase.get_category import GetCategory, GetCategoryRequest
from src.core.category.application.usecase.list_category import ListCategoryRequest, ListCategory
from src.django_project.category_app.repository import DjangoORMCategoryRepository


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryRequest()

        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        response = use_case.execute(request=input)

        categories = [{'id': str(category.id), 'name': category.name, 'description': category.description,
                       'is_active': category.is_active} for category in response.data]

        return Response(status=HTTP_200_OK, data=categories)

    def retrieve(self, request: Request, pk=None) -> Response:
        try:
            category_pk = UUID(pk)
        except ValueError:
            return Response(status=HTTP_400_BAD_REQUEST)

        use_case = GetCategory(repository=DjangoORMCategoryRepository())
        try:
            response = use_case.execute(request=GetCategoryRequest(id=category_pk))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category_data = {
            'id': str(response.id),
            'name': response.name,
            'description': response.description,
            'is_active': response.is_active
        }
        return Response(status=HTTP_200_OK, data=category_data)
