from dataclasses import dataclass, field
from uuid import UUID
import uuid


@dataclass
class Genre:
    name: str
    id: UUID = field(default_factory=uuid.uuid4)
    is_active: bool = True
    categories: set[UUID] = field(default_factory=set)

    def __post_init__(self):
        self.validate()

    def change_name(self, name: str):
        self.name = name
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            raise ValueError('name cannot be longer than 255 characters')
        if not self.name:
            raise ValueError('name cannot be empty')

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()

    def add_category(self, category_id: UUID):
        self.categories.add(category_id)
        self.validate()

    def remove_category(self, category_id: UUID):
        self.categories.discard(category_id)
        self.validate()

    def __str__(self):
        return f'{self.name} (Active: {self.is_active})'

    def __repr__(self):
        return f'<Genre id={self.id} name={self.name}>'

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return self.id == other.id
