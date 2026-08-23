from src.core._shared.events.event import Event
from src.core._shared.events.message_bus import MessageBus
from src.core._shared.application.handler import Handler
from unittest.mock import create_autospec

class DummyEvent(Event):
    pass

class TestMessageBus:
    def test_handle_event(self):
        message_bus = MessageBus()
        dummy_handler = create_autospec(Handler)
        message_bus.handlers[DummyEvent] = [dummy_handler]

        event = DummyEvent()
        message_bus.handle([event])

        dummy_handler.handle.assert_called_once_with(event)

    def test_handle_event_with_exception(self):
        message_bus = MessageBus()
        dummy_handler = create_autospec(Handler)
        dummy_handler.handle.side_effect = Exception("Handler error")
        message_bus.handlers[DummyEvent] = [dummy_handler]

        event = DummyEvent()
        message_bus.handle([event])

        dummy_handler.handle.assert_called_once_with(event)

    def test_handle_event_with_multiple_handlers(self):
        message_bus = MessageBus()
        dummy_handler1 = create_autospec(Handler)
        dummy_handler2 = create_autospec(Handler)
        message_bus.handlers[DummyEvent] = [dummy_handler1, dummy_handler2]

        event = DummyEvent()
        message_bus.handle([event])

        dummy_handler1.handle.assert_called_once_with(event)
        dummy_handler2.handle.assert_called_once_with(event)