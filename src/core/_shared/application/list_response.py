from dataclasses import dataclass, field
from typing import TypeVar, Generic, List

T = TypeVar('T')


@dataclass
class ListOutputMeta:
    current_page: int
    per_page: int
    total: int


@dataclass
class ListResponse(Generic[T]):
    data: List[T]
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)
