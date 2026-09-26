import json
from venv import logger
import pika
from uuid import UUID

from src.core._shared.events.abstract_consumer import AbstractConsumer
from src.core.video.application.usecase.process_audio_video_media import ProcessAudioVideoMedia
from src.core.video.domain.value_objects import MediaStatus, MediaType
from src.core.video.domain.video_repository import VideoRepository


class VideoConvertedRabbitMQConsumer(AbstractConsumer):
    def __init__(self, repository: VideoRepository, host='localhost', queue='videos.converted'):
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None
        self.repository = repository

    def on_message(self, message):
        print(f"Received message: {message}")
        try:
            # Body payload
            message = json.loads(message)

            # Tratamento de erro
            error_message = message["error"]
            if error_message:
                aggregate_id_raw, _ = message["message"]["resource_id"].split(".")
                logger.error(f"Error processing video {aggregate_id_raw}: {error_message}")
                return

            # Serialização do evento
            aggregate_id_raw, media_type_raw = message["video"]["resource_id"].split(".")
            aggregate_id = UUID(aggregate_id_raw)
            media_type = MediaType(media_type_raw)
            encoded_location = message["video"]["encoded_video_folder"]
            status = MediaStatus(message["status"])

            # Execução do caso de uso
            process_audio_video_media_input = ProcessAudioVideoMedia.Input(
                video_id=aggregate_id,
                encoded_location=encoded_location,
                media_type=media_type,
                status=status,
            )
            print("Calling use case with input", process_audio_video_media_input)
            use_case = ProcessAudioVideoMedia(video_repository=self.repository)
            use_case.execute(input=process_audio_video_media_input)
        except Exception as e:
            logger.error(f"Error processing payload {message}", exc_info=True)
            return

    def start(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()

        # Cria a fila se não existir
        self.channel.queue_declare(queue=self.queue)

        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.on_message_callback,
            auto_ack=True,
        )
        print('Consumer started. Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def on_message_callback(self, ch, method, properties, body):
        self.on_message(body)

    def stop(self):
        self.connection.close()
