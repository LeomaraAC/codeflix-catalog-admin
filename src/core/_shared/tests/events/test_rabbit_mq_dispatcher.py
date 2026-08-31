import json
from unittest.mock import MagicMock, call, patch

from src.core._shared.infrastructure.events.rabbit_mq_dispatcher import (
    RabbitMQDispatcher,
)
from src.core.video.application.events.integration_events import (
    AudioVideoMediaUpdatedIntegrationEvent,
)


class TestRabbitMQDispatcher:
    def test_uses_default_configuration(self):
        dispatcher = RabbitMQDispatcher()

        assert dispatcher.host == "localhost"
        assert dispatcher.queue == "videos.new"
        assert dispatcher.connection is None
        assert dispatcher.channel is None

    def test_uses_custom_configuration(self):
        dispatcher = RabbitMQDispatcher(
            host="rabbitmq",
            queue="videos.updated",
        )

        assert dispatcher.host == "rabbitmq"
        assert dispatcher.queue == "videos.updated"

    @patch(
        "src.core._shared.infrastructure.events.rabbit_mq_dispatcher."
        "pika.ConnectionParameters"
    )
    @patch(
        "src.core._shared.infrastructure.events.rabbit_mq_dispatcher."
        "pika.BlockingConnection"
    )
    def test_dispatch_opens_connection_and_publishes_serialized_event(
        self,
        blocking_connection,
        connection_parameters,
    ):
        connection = blocking_connection.return_value
        channel = connection.channel.return_value
        parameters = connection_parameters.return_value
        dispatcher = RabbitMQDispatcher(
            host="rabbitmq",
            queue="videos.updated",
        )
        event = self._create_event()

        dispatcher.dispatch(event)

        connection_parameters.assert_called_once_with(host="rabbitmq")
        blocking_connection.assert_called_once_with(parameters)
        connection.channel.assert_called_once_with()
        channel.queue_declare.assert_called_once_with(queue="videos.updated")
        channel.basic_publish.assert_called_once_with(
            exchange="",
            routing_key="videos.updated",
            body=json.dumps(event.payload),
        )
        assert dispatcher.connection is connection
        assert dispatcher.channel is channel

    @patch(
        "src.core._shared.infrastructure.events.rabbit_mq_dispatcher."
        "pika.ConnectionParameters"
    )
    @patch(
        "src.core._shared.infrastructure.events.rabbit_mq_dispatcher."
        "pika.BlockingConnection"
    )
    def test_dispatch_reuses_connection_and_channel(
        self,
        blocking_connection,
        connection_parameters,
    ):
        connection = blocking_connection.return_value
        channel = connection.channel.return_value
        dispatcher = RabbitMQDispatcher(queue="videos.updated")
        first_event = self._create_event(resource_id="first-video")
        second_event = self._create_event(resource_id="second-video")

        dispatcher.dispatch(first_event)
        dispatcher.dispatch(second_event)

        connection_parameters.assert_called_once_with(host="localhost")
        blocking_connection.assert_called_once_with(
            connection_parameters.return_value,
        )
        connection.channel.assert_called_once_with()
        channel.queue_declare.assert_called_once_with(queue="videos.updated")
        assert channel.basic_publish.call_args_list == [
            call(
                exchange="",
                routing_key="videos.updated",
                body=json.dumps(first_event.payload),
            ),
            call(
                exchange="",
                routing_key="videos.updated",
                body=json.dumps(second_event.payload),
            ),
        ]

    def test_close_closes_connection_and_clears_internal_state(self):
        dispatcher = RabbitMQDispatcher()
        connection = MagicMock()
        dispatcher.connection = connection
        dispatcher.channel = MagicMock()

        dispatcher.close()

        connection.close.assert_called_once_with()
        assert dispatcher.connection is None
        assert dispatcher.channel is None

    def test_close_without_connection_has_no_effect(self):
        dispatcher = RabbitMQDispatcher()

        dispatcher.close()

        assert dispatcher.connection is None
        assert dispatcher.channel is None

    @patch(
        "src.core._shared.infrastructure.events.rabbit_mq_dispatcher."
        "pika.ConnectionParameters"
    )
    @patch(
        "src.core._shared.infrastructure.events.rabbit_mq_dispatcher."
        "pika.BlockingConnection"
    )
    def test_dispatch_after_close_opens_new_connection(
        self,
        blocking_connection,
        connection_parameters,
    ):
        first_connection = MagicMock()
        second_connection = MagicMock()
        blocking_connection.side_effect = [first_connection, second_connection]
        dispatcher = RabbitMQDispatcher()
        event = self._create_event()

        dispatcher.dispatch(event)
        dispatcher.close()
        dispatcher.dispatch(event)

        assert blocking_connection.call_args_list == [
            call(connection_parameters.return_value),
            call(connection_parameters.return_value),
        ]
        first_connection.close.assert_called_once_with()
        first_connection.channel.assert_called_once_with()
        second_connection.channel.assert_called_once_with()
        assert dispatcher.connection is second_connection
        assert dispatcher.channel is second_connection.channel.return_value

    @staticmethod
    def _create_event(
        resource_id: str = "video-id",
    ) -> AudioVideoMediaUpdatedIntegrationEvent:
        return AudioVideoMediaUpdatedIntegrationEvent(
            resource_id=resource_id,
            file_path="videos/video.mp4",
        )
