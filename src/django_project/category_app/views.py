from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        return Response(status=HTTP_200_OK, data=[
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Films",
                "description": "Category for films",
                "is_active": True
            },
            {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "Series",
                "description": "Category for series",
                "is_active": False
            }
        ])