import uuid


class Category:
    def __init__(self, name: str, id: uuid.UUID = None, description: str = "", is_active: bool = True):
        self.name = name
        self.validate()

        self.id = id or uuid.uuid4()
        self.description = description
        self.is_active = is_active

    def update_category(self, name: str, description: str):
        self.name = name
        self.validate()
        self.description = description

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255 characters")
        if not self.name:
            raise ValueError("name cannot be empty")

    def __str__(self):
        return f'{self.name} - {self.description} (Active: {self.is_active})'

    def __repr__(self):
        return f'<Category id={self.id} name={self.name}>'