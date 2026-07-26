from decimal import Decimal
from uuid import UUID, uuid4

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound
from src.core.video.application.usecase.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.infra.in_memory_video_repository import InMemoryVideoRepository




class TestCreateVideoWithoutMedia:
	def test_create_video_with_valid_data(self):
		video_repository = InMemoryVideoRepository()
		category = Category(name='Movies')
		genre = Genre(name='Action')
		cast_member = CastMember(name='Keanu Reeves', type=CastMemberType.ACTOR)
		use_case = self._build_use_case(
			video_repository=video_repository,
			categories=[category],
			genres=[genre],
			cast_members=[cast_member],
		)

		response = use_case.execute(
			self._build_input(
				categories={category.id},
				genres={genre.id},
				cast_members={cast_member.id},
			)
		)

		persisted_video = video_repository.videos[0]

		assert response is not None
		assert isinstance(response.id, UUID)
		assert len(video_repository.videos) == 1
		assert persisted_video.id == response.id
		assert persisted_video.title == 'John Wick'
		assert persisted_video.published is False
		assert persisted_video.categories == {category.id}
		assert persisted_video.genres == {genre.id}
		assert persisted_video.cast_members == {cast_member.id}

	def test_raise_exception_when_categories_and_cast_members_are_invalid(self):
		video_repository = InMemoryVideoRepository()
		genre = Genre(name='Action')
		use_case = self._build_use_case(
			video_repository=video_repository,
			genres=[genre],
		)

		with pytest.raises(RelatedEntitiesNotFound) as exc_info:
			use_case.execute(
				self._build_input(
					categories={uuid4()},
					genres={genre.id},
					cast_members={uuid4()},
				)
			)

		assert 'Categories with provided IDs not found' in str(exc_info.value)
		assert 'Cast members with provided IDs not found' in str(exc_info.value)
		assert len(video_repository.videos) == 0

	def test_raise_exception_when_genres_are_invalid(self):
		video_repository = InMemoryVideoRepository()
		category = Category(name='Movies')
		cast_member = CastMember(name='Keanu Reeves', type=CastMemberType.ACTOR)
		use_case = self._build_use_case(
			video_repository=video_repository,
			categories=[category],
			cast_members=[cast_member],
		)

		with pytest.raises(RelatedEntitiesNotFound, match='Genres with provided IDs not found'):
			use_case.execute(
				self._build_input(
					categories={category.id},
					genres={uuid4()},
					cast_members={cast_member.id},
				)
			)

		assert len(video_repository.videos) == 0

	def test_raise_exception_when_video_data_is_invalid(self):
		video_repository = InMemoryVideoRepository()
		category = Category(name='Movies')
		genre = Genre(name='Action')
		cast_member = CastMember(name='Keanu Reeves', type=CastMemberType.ACTOR)
		use_case = self._build_use_case(
			video_repository=video_repository,
			categories=[category],
			genres=[genre],
			cast_members=[cast_member],
		)

		with pytest.raises(InvalidVideo) as exc_info:
			use_case.execute(
				self._build_input(
					title='',
					categories={category.id},
					genres={genre.id},
					cast_members={cast_member.id},
				)
			)

		assert 'Title cannot be empty' in str(exc_info.value)
		assert len(video_repository.videos) == 0

	@staticmethod
	def _build_use_case(
		video_repository: VideoRepository | None = None,
		categories: list[Category] | None = None,
		genres: list[Genre] | None = None,
		cast_members: list[CastMember] | None = None,
	) -> CreateVideoWithoutMedia:
		return CreateVideoWithoutMedia(
			video_repository=video_repository or InMemoryVideoRepository(),
			category_repository=InMemoryCategoryRepository(categories or []),
			genre_repository=InMemoryGenreRepository(genres or []),
			cast_member_repository=InMemoryCastMemberRepository(cast_members or []),
		)

	@staticmethod
	def _build_input(
		title: str = 'John Wick',
		description: str = 'Action movie',
		launch_year: int = 2014,
		duration: Decimal = Decimal('120'),
		rating: Rating = Rating.AGE_16,
		categories: set[UUID] | None = None,
		genres: set[UUID] | None = None,
		cast_members: set[UUID] | None = None,
	) -> CreateVideoWithoutMedia.Input:
		return CreateVideoWithoutMedia.Input(
			title=title,
			description=description,
			launch_year=launch_year,
			duration=duration,
			rating=rating,
			categories=categories or set(),
			genres=genres or set(),
			cast_members=cast_members or set(),
		)
