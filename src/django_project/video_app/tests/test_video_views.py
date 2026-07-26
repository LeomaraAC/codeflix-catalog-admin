from decimal import Decimal

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository


@pytest.fixture
def category_movie() -> Category:
    return Category(name='Movie', description='Movie category')


@pytest.fixture
def category_repository(category_movie: Category) -> DjangoORMCategoryRepository:
    repository = DjangoORMCategoryRepository()
    repository.save(category_movie)
    return repository


@pytest.fixture
def genre_action(category_movie: Category, category_repository: DjangoORMCategoryRepository) -> Genre:
    return Genre(name='Action', categories={category_movie.id})


@pytest.fixture
def genre_repository(genre_action: Genre) -> DjangoORMGenreRepository:
    repository = DjangoORMGenreRepository()
    repository.save(genre_action)
    return repository


@pytest.fixture
def cast_member_keanu() -> CastMember:
    return CastMember(name='Keanu Reeves', type=CastMemberType.ACTOR)


@pytest.fixture
def cast_member_repository(cast_member_keanu: CastMember) -> DjangoORMCastMemberRepository:
    repository = DjangoORMCastMemberRepository()
    repository.save(cast_member_keanu)
    return repository


@pytest.fixture
def persisted_video(
    category_movie: Category,
    category_repository: DjangoORMCategoryRepository,
    genre_action: Genre,
    genre_repository: DjangoORMGenreRepository,
    cast_member_keanu: CastMember,
    cast_member_repository: DjangoORMCastMemberRepository,
) -> Video:
    video = Video(
        title='John Wick',
        description='Action movie',
        launch_year=2014,
        duration=Decimal('120.50'),
        published=False,
        rating=Rating.AGE_16,
        categories={category_movie.id},
        genres={genre_action.id},
        cast_members={cast_member_keanu.id},
    )
    DjangoORMVideoRepository().save(video)
    return video


@pytest.mark.django_db
class TestCreateVideoAPI:
    def test_when_payload_is_valid_then_return_201(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
        genre_action: Genre,
        genre_repository: DjangoORMGenreRepository,
        cast_member_keanu: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        payload = {
            'title': 'John Wick',
            'description': 'Action movie',
            'launch_year': 2014,
            'duration': '120.50',
            'rating': Rating.AGE_16.name,
            'categories': [str(category_movie.id)],
            'genres': [str(genre_action.id)],
            'cast_members': [str(cast_member_keanu.id)],
        }

        response = APIClient().post('/api/videos/', data=payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data

        video = DjangoORMVideoRepository().get_by_id(response.data['id'])

        assert video is not None
        assert video.title == payload['title']
        assert video.description == payload['description']
        assert video.launch_year == payload['launch_year']
        assert video.duration == Decimal(payload['duration'])
        assert video.published is False
        assert video.rating == Rating.AGE_16
        assert video.categories == {category_movie.id}
        assert video.genres == {genre_action.id}
        assert video.cast_members == {cast_member_keanu.id}

    def test_when_related_entities_do_not_exist_then_return_400(self) -> None:
        payload = {
            'title': 'John Wick',
            'description': 'Action movie',
            'launch_year': 2014,
            'duration': '120.50',
            'rating': Rating.AGE_16.name,
            'categories': ['95d0df35-0dbf-4e5d-a7e8-ee4fdf99597b'],
            'genres': ['e76ce838-fc0c-45a7-a164-ed5685686a4b'],
            'cast_members': ['dbd50345-dab7-4e93-8452-07a90c7c92ec'],
        }

        response = APIClient().post('/api/videos/', data=payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Categories with provided IDs not found' in response.data['error']
        assert 'Genres with provided IDs not found' in response.data['error']
        assert 'Cast members with provided IDs not found' in response.data['error']


@pytest.mark.django_db
class TestListVideoAPI:
    def test_when_no_videos_exist_then_return_empty_list(self) -> None:
        response = APIClient().get('/api/videos/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'data': [],
            'meta': {
                'current_page': 1,
                'per_page': 2,
                'total': 0,
            },
        }

    def test_when_videos_exist_then_return_paginated_list(self, persisted_video: Video) -> None:
        response = APIClient().get('/api/videos/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'data': [
                {
                    'id': str(persisted_video.id),
                    'title': persisted_video.title,
                    'description': persisted_video.description,
                    'launch_year': persisted_video.launch_year,
                    'duration': '120.50',
                    'published': persisted_video.published,
                    'rating': persisted_video.rating.name,
                    'categories': [str(next(iter(persisted_video.categories)))],
                    'genres': [str(next(iter(persisted_video.genres)))],
                    'cast_members': [str(next(iter(persisted_video.cast_members)))],
                }
            ],
            'meta': {
                'current_page': 1,
                'per_page': 2,
                'total': 1,
            },
        }


@pytest.mark.django_db
class TestRetrieveVideoAPI:
    def test_when_video_exists_then_return_200(self, persisted_video: Video) -> None:
        response = APIClient().get(f'/api/videos/{persisted_video.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'data': {
                'id': str(persisted_video.id),
                'title': persisted_video.title,
                'description': persisted_video.description,
                'launch_year': persisted_video.launch_year,
                'duration': '120.50',
                'published': persisted_video.published,
                'rating': persisted_video.rating.name,
                'categories': [str(next(iter(persisted_video.categories)))],
                'genres': [str(next(iter(persisted_video.genres)))],
                'cast_members': [str(next(iter(persisted_video.cast_members)))],
            }
        }

    def test_when_video_does_not_exist_then_return_404(self) -> None:
        response = APIClient().get('/api/videos/95d0df35-0dbf-4e5d-a7e8-ee4fdf99597b/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
