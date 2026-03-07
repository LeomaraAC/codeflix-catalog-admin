import uuid

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.fixture
def category_movie():
    return Category(name='Movie', description='All about movies')


@pytest.fixture
def category_documentary():
    return Category(name='Documentary', description='All about documentaries')


@pytest.fixture
def category_repository(category_movie, category_documentary) -> DjangoORMCategoryRepository:
    repo = DjangoORMCategoryRepository()
    repo.save(category_movie)
    repo.save(category_documentary)
    return repo


@pytest.fixture
def genre_romance(category_movie, category_documentary) -> Genre:
    return Genre(name='Romance', is_active=True, categories={category_movie.id, category_documentary.id})


@pytest.fixture
def genre_drama() -> Genre:
    return Genre(name='Drama', is_active=True)


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.mark.django_db
class TestListGenreAPI:
    def test_list_genres_and_categories(
            self,
            genre_repository: DjangoORMGenreRepository,
            category_repository: DjangoORMCategoryRepository,
            genre_romance: Genre,
            genre_drama: Genre
    ):
        # Save genres
        genre_repository.save(genre_romance)
        genre_repository.save(genre_drama)

        # Make API call to list genres
        response = APIClient().get('/api/genres/')

        # Verify response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']

        romance_data = response.data['data'][0]
        drama_data = response.data['data'][1]

        assert romance_data['id'] == str(genre_romance.id)
        assert romance_data['name'] == genre_romance.name
        assert romance_data['is_active'] == genre_romance.is_active
        assert set(romance_data['categories']) == {str(cat_id) for cat_id in genre_romance.categories}

        assert drama_data['id'] == str(genre_drama.id)
        assert drama_data['name'] == genre_drama.name
        assert drama_data['is_active'] == genre_drama.is_active
        assert drama_data['categories'] == []


@pytest.mark.django_db
class TestCreateGenreAPI:
    def test_create_genre_with_categories(
            self,
            category_repository: DjangoORMCategoryRepository,
            category_movie: Category,
            category_documentary: Category,
            genre_repository: DjangoORMGenreRepository
    ):
        # Prepare payload
        payload = {
            'name': 'Sci-Fi',
            'category_ids': [str(category_movie.id), str(category_documentary.id)]
        }

        # Make API call to create genre
        response = APIClient().post('/api/genres/', data=payload, format='json')

        # Verify response
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id']

        created_genre_id = response.data['id']
        saved_genre = genre_repository.get_by_id(id=created_genre_id)

        assert saved_genre.name == payload['name']
        assert saved_genre.is_active == True
        assert saved_genre.categories == {category_movie.id, category_documentary.id}


@pytest.mark.django_db
class TestDeleteGenreAPI:
    def test_delete_genre(self, genre_repository: DjangoORMGenreRepository, genre_romance: Genre):
        # Save genre
        genre_repository.save(genre_romance)

        # Make API call to delete genre
        response = APIClient().delete(f'/api/genres/{genre_romance.id}/')

        # Verify response
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert genre_repository.get_by_id(id=genre_romance.id) is None

    def test_when_genre_does_nost_exist_then_return_404(self):

        # Make API call to delete non-existent genre
        response = APIClient().delete(f'/api/genres/{uuid.uuid4()}/')

        # Verify response
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_pk_is_not_uuid_then_return_400(self):
        # Make API call to delete genre with invalid pk
        response = APIClient().delete('/api/genres/invalid-uuid/')

        # Verify response
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestUpdateGenreAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        genre_repository.save(genre_romance)

        url = f'/api/genres/{str(genre_romance.id)}/'
        data = {
            'name': 'Drama',
            'is_active': True,
            'category_ids': [category_documentary.id],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_genre = genre_repository.get_by_id(genre_romance.id)
        assert updated_genre.name == 'Drama'
        assert updated_genre.is_active is True
        assert updated_genre.categories == {category_documentary.id}

    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_drama: Genre,
    ) -> None:
        url = f'/api/genres/{str(genre_drama.id)}/'
        data = {
            'name': '',
            'is_active': True,
            'categories': [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'name': ['This field may not be blank.']}

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        genre_repository.save(genre_romance)

        url = f'/api/genres/{str(genre_romance.id)}/'
        data = {
            'name': 'Romance',
            'is_active': True,
            'category_ids': [uuid.uuid4()],  # non-existent category
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Categories not found' in response.data['error']

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        url = f'/api/genres/{str(uuid.uuid4())}/'
        data = {
            'name': 'Romance',
            'is_active': True,
            'categories': [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
