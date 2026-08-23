from typing import Type
from src.core._shared.events.absctract_message_bus import AbstractMessageBus
from src.core._shared.events.event import TEvent, Event
from src.core._shared.application.handler import Handler


class MessageBus(AbstractMessageBus):
    def __init__(self):
        self.handlers: dict[Type[TEvent], list[Handler[TEvent]]] = {}

    def handle(self, event: list[Event]):
        for e in event:
            for handler in self.handlers.get(type(e), []):
                try:
                    handler.handle(e)
                except Exception as ex:
                    print(f"Error handling event {e}: {ex}")