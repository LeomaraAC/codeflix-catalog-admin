from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from src.core._shared.events.message_bus import MessageBus
from src.core._shared.infrastructure.storage.local_storage import LocalStorage
from src.core.video.application.exceptions import RelatedEntitiesNotFound, InvalidVideo, VideoNotFound
from src.core.video.application.usecase.get_video import GetVideo
from src.core.video.application.usecase.list_video import ListVideo
from src.core.video.application.usecase.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.application.usecase.upload_video import UploadVideo
from src.django_project.video_app.serializers import CreateVideoInputSerializer, CreateVideoOutputSerializer, \
    ListVideoOutputSerializer, RetrieveVideoInputSerializer, RetrieveVideoOutputSerializer
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository

class VideoViewSet(viewsets.ViewSet):

    def list(self, request: Request) -> Response:
        order_by = request.query_params.get('order_by', 'title')
        current_page = int(request.query_params.get('current_page', 1))
        usecase = ListVideo(repository=DjangoORMVideoRepository())
        output = usecase.execute(ListVideo.Input(order_by=order_by, current_page=current_page))

        return Response(status=HTTP_200_OK, data=ListVideoOutputSerializer(instance=output).data)

    def retrieve(self, request: Request, pk=None) -> Response:
        serializer = RetrieveVideoInputSerializer(data={'id': pk})
        serializer.is_valid(raise_exception=True)

        usecase = GetVideo(repository=DjangoORMVideoRepository())
        try:
            output = usecase.execute(GetVideo.Input(id=serializer.validated_data['id']))
        except VideoNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_200_OK, data=RetrieveVideoOutputSerializer(instance=output).data)

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

    def partial_update(self, request: Request, pk: UUID =None) -> Response:
        file = request.FILES['video_file']
        content = file.read()
        content_type = file.content_type

        usecase = UploadVideo(
            video_repository=DjangoORMVideoRepository(),
            storage_service=LocalStorage(),
            message_bus=MessageBus(),
        )
        try:
            usecase.execute(UploadVideo.Input(video_id=pk, file_name=file.name, content=content, content_type=content_type))
        except VideoNotFound:
            return Response(status=HTTP_404_NOT_FOUND, data={'error': f'Video with id {pk} not found'})

        return Response(status=HTTP_200_OK)
