from abc import ABC, abstractmethod
from src.core._shared.events.event import Event

class AbstractMessageBus(ABC):
    @abstractmethod
    def handle(self, event: list[Event]):
        raise NotImplementedError("Subclasses must implement the handle method.")