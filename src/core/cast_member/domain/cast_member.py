from dataclasses import dataclass
from enum import StrEnum

from src.core._shared.entity import Entity


class CastMemberType(StrEnum):
    ACTOR = "ACTOR"
    DIRECTOR = "DIRECTOR"


@dataclass
class CastMember(Entity):
    name: str
    type: CastMemberType

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.name:
            self.notification.add_error("name cannot be empty")
        if len(self.name) > 255:
            self.notification.add_error("name cannot be longer than 255 characters")
        if self.type not in CastMemberType:
            self.notification.add_error("type must be either ACTOR or DIRECTOR")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def update(self, name: str, type: CastMemberType):
        self.name = name
        self.type = type
        self.validate()
