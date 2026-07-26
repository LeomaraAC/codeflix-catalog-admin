from decimal import Decimal
from unittest.mock import create_autospec

from src.core._shared.application.list_response import ListResponse, ListOutputMeta
from src.core.video.application.usecase.list_video import ListVideo
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository


class TestListVideo:
    def test_when_no_video_then_return_empty_list(self):
        mock_repository = create_autospec(VideoRepository)
        mock_repository.list.return_value = []

        use_case = ListVideo(repository=mock_repository)
        response = use_case.execute(ListVideo.Input())

        assert response == ListResponse(data=[], meta=ListOutputMeta(current_page=1, per_page=2, total=0))

    def test_when_videos_exist_then_return_mapped_list(self):
        first_video = Video(
            title='Batman Begins',
            description='Origin story',
            launch_year=2005,
            duration=Decimal('140.00'),
            published=False,
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        second_video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('101.00'),
            published=True,
            rating=Rating.AGE_16,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        mock_repository = create_autospec(VideoRepository)
        mock_repository.list.return_value = [first_video, second_video]

        use_case = ListVideo(repository=mock_repository)
        response = use_case.execute(ListVideo.Input())

        assert response == ListResponse(
            data=[
                ListVideo.Output(
                    id=first_video.id,
                    title=first_video.title,
                    description=first_video.description,
                    launch_year=first_video.launch_year,
                    duration=first_video.duration,
                    published=first_video.published,
                    rating=first_video.rating,
                    categories=first_video.categories,
                    genres=first_video.genres,
                    cast_members=first_video.cast_members,
                ),
                ListVideo.Output(
                    id=second_video.id,
                    title=second_video.title,
                    description=second_video.description,
                    launch_year=second_video.launch_year,
                    duration=second_video.duration,
                    published=second_video.published,
                    rating=second_video.rating,
                    categories=second_video.categories,
                    genres=second_video.genres,
                    cast_members=second_video.cast_members,
                ),
            ],
            meta=ListOutputMeta(current_page=1, per_page=2, total=2),
        )

    def test_when_paginating_videos_then_return_requested_page(self):
        first_video = Video(
            title='Avatar',
            description='Sci-fi movie',
            launch_year=2009,
            duration=Decimal('162.00'),
            published=False,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        second_video = Video(
            title='Batman Begins',
            description='Origin story',
            launch_year=2005,
            duration=Decimal('140.00'),
            published=False,
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        third_video = Video(
            title='John Wick',
            description='Action movie',
            launch_year=2014,
            duration=Decimal('101.00'),
            published=True,
            rating=Rating.AGE_16,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        mock_repository = create_autospec(VideoRepository)
        mock_repository.list.return_value = [third_video, first_video, second_video]

        use_case = ListVideo(repository=mock_repository)
        response = use_case.execute(ListVideo.Input(order_by='title', current_page=2))

        assert response.data == [
            ListVideo.Output(
                id=third_video.id,
                title=third_video.title,
                description=third_video.description,
                launch_year=third_video.launch_year,
                duration=third_video.duration,
                published=third_video.published,
                rating=third_video.rating,
                categories=third_video.categories,
                genres=third_video.genres,
                cast_members=third_video.cast_members,
            )
        ]
        assert response.meta == ListOutputMeta(current_page=2, per_page=2, total=3)