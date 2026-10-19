import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.category.domain.category import Category
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.fixture
def jane() -> CastMember:
    return CastMember(name='Jane Smith', type=CastMemberType.ACTOR)


@pytest.fixture
def john() -> CastMember:
    return CastMember(name='John Doe', type=CastMemberType.DIRECTOR)


@pytest.fixture
def category_movie() -> Category:
    return Category(name='Movie', description='All about movies')
