from decimal import Decimal

from src.core.video.application.usecase.list_video import ListVideo
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository


class TestListVideo:
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
        repository = InMemoryVideoRepository()
        repository.save(first_video)
        repository.save(second_video)

        use_case = ListVideo(repository=repository)
        response = use_case.execute(ListVideo.Input())

        assert len(response.data) == 2
        assert ListVideo.Output(
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
        ) in response.data
        assert ListVideo.Output(
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
        ) in response.data

    def test_when_repository_is_empty_then_return_empty_list(self):
        use_case = ListVideo(repository=InMemoryVideoRepository())
        response = use_case.execute(ListVideo.Input())

        assert response.data == []

    def test_when_paginating_videos_then_return_requested_page(self):
        repository = InMemoryVideoRepository()
        repository.save(
            Video(
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
        )
        repository.save(
            Video(
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
        )
        john_wick = Video(
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
        repository.save(john_wick)

        use_case = ListVideo(repository=repository)
        response = use_case.execute(ListVideo.Input(order_by='title', current_page=2))

        assert response.data == [
            ListVideo.Output(
                id=john_wick.id,
                title=john_wick.title,
                description=john_wick.description,
                launch_year=john_wick.launch_year,
                duration=john_wick.duration,
                published=john_wick.published,
                rating=john_wick.rating,
                categories=john_wick.categories,
                genres=john_wick.genres,
                cast_members=john_wick.cast_members,
            )
        ]