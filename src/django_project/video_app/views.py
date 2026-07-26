from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from src.core.video.application.usecase.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.application.exceptions import RelatedEntitiesNotFound, InvalidVideo
from src.django_project.video_app.serializers import CreateVideoInputSerializer, CreateVideoOutputSerializer
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository

class VideoViewSet(viewsets.ViewSet):

    def create(self, request: Request) -> Response:
        serializer = CreateVideoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateVideoWithoutMedia.Input(**serializer.validated_data)
        usecase = CreateVideoWithoutMedia(video_repository=DjangoORMVideoRepository(),
                                          category_repository=DjangoORMCategoryRepository(),
                                          genre_repository=DjangoORMGenreRepository(),
                                          cast_member_repository=DjangoORMCastMemberRepository())
        try:
            output: CreateVideoWithoutMedia.Output = usecase.execute(input)
        except (RelatedEntitiesNotFound, InvalidVideo) as err:
            return Response(status=HTTP_400_BAD_REQUEST, data={'error': str(err)})
        
        return Response(status=HTTP_201_CREATED, data=CreateVideoOutputSerializer(output).data)