from dataclasses import dataclass, field
from uuid import UUID
import uuid


@dataclass
class Category:
    name: str
    id: UUID = field(default_factory=uuid.uuid4)
    description: str = ""
    is_active: bool = True

    def __post_init__(self):
        self.validate()

    def update_category(self, name: str, description: str):
        self.name = name
        self.validate()
        self.description = description

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255 characters")
        if not self.name:
            raise ValueError("name cannot be empty")
        
    def activate(self):
        self.is_active = True
        self.validate()
    
    def deactivate(self):
        self.is_active = False
        self.validate()

    def __str__(self):
        return f'{self.name} - {self.description} (Active: {self.is_active})'

    def __repr__(self):
        return f'<Category id={self.id} name={self.name}>'
    
    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id