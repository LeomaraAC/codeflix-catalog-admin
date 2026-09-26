from django.core.management.base import BaseCommand

from src.core.video.infra.video_converted_rabbitmq_consumer import VideoConvertedRabbitMQConsumer
from src.django_project.video_app.repository import DjangoORMVideoRepository

class Command(BaseCommand):
    help = 'Starts the consumer to process converted videos'

    def handle(self, *args, **options):
        

        repository = DjangoORMVideoRepository()
        consumer = VideoConvertedRabbitMQConsumer(repository=repository)
        consumer.start()