from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.domain.entity import Entity
from src.core.video.domain.value_objects import Rating, ImageMedia, AudioVideoMedia


@dataclass
class Video(Entity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    published: bool
    rating: Rating

    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]

    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.title) > 255:
            self.notification.add_error('Title cannot be longer than 255 characters')

        if not self.title:
            self.notification.add_error('Title cannot be empty')

        if self.duration < 0:
            self.notification.add_error('Duration cannot be negative')

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def update(self, title: str, description: str, launch_year: int, duration: Decimal, published: bool, rating: Rating):
        self.title = title
        self.description = description
        self.launch_year = launch_year
        self.duration = duration
        self.published = published
        self.rating = rating

        self.validate()

    def add_category(self, category: UUID):
        self.categories.add(category)
        self.validate()

    def add_genre(self, genre: UUID):
        self.genres.add(genre)
        self.validate()

    def add_cast_member(self, cast_member: UUID):
        self.cast_members.add(cast_member)
        self.validate()

    def update_thumbnail(self, thumbnail: ImageMedia):
        self.thumbnail = thumbnail
        self.validate()

    def update_thumbnail_half(self, thumbnail_half: ImageMedia):
        self.thumbnail_half = thumbnail_half
        self.validate()

    def update_trailer(self, trailer: AudioVideoMedia):
        self.trailer = trailer
        self.validate()

    def update_video(self, video: AudioVideoMedia):
        self.video = video
        self.validate()

    def update_banner(self, banner: ImageMedia):
        self.banner = banner
        self.validate()
