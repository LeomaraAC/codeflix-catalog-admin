import json
from unittest.mock import MagicMock, call, create_autospec, patch
from uuid import UUID

import pytest

from src.core.video.application.usecase.process_audio_video_media import ProcessAudioVideoMedia
from src.core.video.domain.value_objects import MediaStatus, MediaType
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.infra.video_converted_rabbitmq_consumer import VideoConvertedRabbitMQConsumer


CONSUMER_MODULE = "src.core.video.infra.video_converted_rabbitmq_consumer"
VIDEO_ID = UUID("fcd84715-2844-4a1c-b0a0-70817abf55c7")


@pytest.fixture
def repository() -> VideoRepository:
    return create_autospec(VideoRepository, instance=True)


@pytest.fixture
def consumer(repository) -> VideoConvertedRabbitMQConsumer:
    return VideoConvertedRabbitMQConsumer(repository=repository)


@pytest.fixture
def use_case():
    with patch(f"{CONSUMER_MODULE}.ProcessAudioVideoMedia", autospec=True) as mock:
        mock.Input = ProcessAudioVideoMedia.Input
        yield mock


@pytest.fixture
def logger():
    with patch(f"{CONSUMER_MODULE}.logger") as mock:
        yield mock


@pytest.fixture
def payload():
    return {
        "error": "",
        "video": {
            "resource_id": f"{VIDEO_ID}.VIDEO",
            "encoded_video_folder": "videos/encoded",
        },
        "status": "COMPLETED",
    }


class TestVideoConvertedRabbitMQConsumer:
    @pytest.mark.parametrize(
        "configuration, expected_host, expected_queue",
        [
            ({}, "localhost", "videos.converted"),
            ({"host": "rabbitmq", "queue": "videos.processed"}, "rabbitmq", "videos.processed"),
        ],
        ids=["defaults", "custom"],
    )
    def test_configuration(self, repository: VideoRepository, configuration: dict[str, str], expected_host: str, expected_queue: str):
        consumer = VideoConvertedRabbitMQConsumer(repository=repository, **configuration)

        assert consumer.host == expected_host
        assert consumer.queue == expected_queue
        assert consumer.repository is repository
        assert consumer.connection is None
        assert consumer.channel is None

    @patch(f"{CONSUMER_MODULE}.pika.ConnectionParameters")
    @patch(f"{CONSUMER_MODULE}.pika.BlockingConnection")
    def test_start_connects_and_consumes_with_auto_ack(
        self, blocking_connection, connection_parameters, repository: VideoRepository
    ):
        consumer = VideoConvertedRabbitMQConsumer(
            repository=repository, host="rabbitmq", queue="videos.processed"
        )
        connection = blocking_connection.return_value
        channel = connection.channel.return_value

        consumer.start()

        connection_parameters.assert_called_once_with("rabbitmq")
        blocking_connection.assert_called_once_with(connection_parameters.return_value)
        connection.channel.assert_called_once_with()
        assert consumer.connection is connection
        assert consumer.channel is channel
        assert channel.mock_calls == [
            call.queue_declare(queue="videos.processed"),
            call.basic_consume(
                queue="videos.processed",
                on_message_callback=consumer.on_message_callback,
                auto_ack=True,
            ),
            call.start_consuming(),
        ]

    def test_callback_forwards_body(self, consumer):
        body = b'{"error": "conversion failed"}'

        with patch.object(consumer, "on_message") as on_message:
            consumer.on_message_callback(MagicMock(), MagicMock(), MagicMock(), body)

        on_message.assert_called_once_with(body)

    @pytest.mark.parametrize("media_type", [MediaType.VIDEO, MediaType.TRAILER])
    def test_valid_message_executes_use_case(
        self, consumer, repository, use_case, logger, payload, media_type
    ):
        payload["video"]["resource_id"] = f"{VIDEO_ID}.{media_type.value}"

        consumer.on_message(json.dumps(payload).encode())

        use_case.assert_called_once_with(video_repository=repository)
        use_case.return_value.execute.assert_called_once_with(
            input=ProcessAudioVideoMedia.Input(
                video_id=VIDEO_ID,
                encoded_location="videos/encoded",
                media_type=media_type,
                status=MediaStatus.COMPLETED,
            )
        )
        received_input = use_case.return_value.execute.call_args.kwargs["input"]
        assert isinstance(received_input, ProcessAudioVideoMedia.Input)
        assert isinstance(received_input.video_id, UUID)
        assert received_input.media_type is media_type
        assert received_input.status is MediaStatus.COMPLETED
        logger.error.assert_not_called()

    def test_reported_error_is_logged_without_executing_use_case(
        self, consumer, use_case, logger
    ):
        payload = {
            "error": "conversion failed",
            "message": {"resource_id": f"{VIDEO_ID}.VIDEO"},
        }

        consumer.on_message(json.dumps(payload).encode())

        logger.error.assert_called_once_with(
            f"Error processing video {VIDEO_ID}: conversion failed"
        )
        use_case.assert_not_called()
        use_case.return_value.execute.assert_not_called()

    @pytest.mark.parametrize(
        "invalid_field, invalid_value",
        [
            ("json", "{invalid json"),
            ("missing_field", "encoded_video_folder"),
            ("resource_id", str(VIDEO_ID)),
            ("resource_id", "invalid-uuid.VIDEO"),
            ("resource_id", f"{VIDEO_ID}.UNKNOWN"),
            ("status", "UNKNOWN"),
        ],
        ids=["invalid-json", "missing-field", "malformed-resource-id", "invalid-uuid", "unknown-media-type", "unknown-status"],
    )
    def test_invalid_payload_is_logged_without_executing_use_case(
        self, consumer, use_case, logger, payload, invalid_field, invalid_value
    ):
        if invalid_field == "missing_field":
            del payload["video"][invalid_value]
        elif invalid_field == "resource_id":
            payload["video"]["resource_id"] = invalid_value
        elif invalid_field == "status":
            payload["status"] = invalid_value

        body = invalid_value if invalid_field == "json" else json.dumps(payload)
        logged_payload = body if invalid_field == "json" else payload

        consumer.on_message(body)

        logger.error.assert_called_once_with(
            f"Error processing payload {logged_payload}", exc_info=True
        )
        use_case.assert_not_called()
        use_case.return_value.execute.assert_not_called()

    def test_use_case_failure_is_logged_without_propagating(
        self, consumer, repository, use_case, logger, payload
    ):
        use_case.return_value.execute.side_effect = RuntimeError("processing failed")

        consumer.on_message(json.dumps(payload))

        use_case.assert_called_once_with(video_repository=repository)
        use_case.return_value.execute.assert_called_once()
        logger.error.assert_called_once_with(
            f"Error processing payload {payload}", exc_info=True
        )

    def test_stop_closes_existing_connection(self, consumer):
        connection = MagicMock()
        consumer.connection = connection

        consumer.stop()

        connection.close.assert_called_once_with()
