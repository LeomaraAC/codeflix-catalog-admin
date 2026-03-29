import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID


class CastMemberType(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"

@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.__validate()

    def __validate(self):
        if not self.name:
            raise ValueError("name cannot be empty")
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255 characters")
        if self.type not in CastMemberType:
            raise ValueError("type must be either ACTOR or DIRECTOR")

    def update(self, name: str, type: CastMemberType):
        self.name = name
        self.type = type
        self.__validate()
