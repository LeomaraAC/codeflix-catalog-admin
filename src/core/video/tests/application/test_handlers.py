from unittest.mock import create_autospec

from src.core._shared.events.event_dispatcher import EventDispatcher
from src.core.video.application.events.handlers import (
    PublishAudioVideoMediaUpdatedHandler,
)
from src.core.video.application.events.integration_events import (
    AudioVideoMediaUpdatedIntegrationEvent,
)


class TestPublishAudioVideoMediaUpdatedHandler:
    def test_dispatches_audio_video_media_updated_event(self):
        event_dispatcher = create_autospec(EventDispatcher, instance=True)
        handler = PublishAudioVideoMediaUpdatedHandler(
            event_dispatcher=event_dispatcher,
        )
        event = AudioVideoMediaUpdatedIntegrationEvent(
            resource_id="video-id",
            file_path="videos/video.mp4",
        )

        handler.handle(event)

        event_dispatcher.dispatch.assert_called_once_with(event)
