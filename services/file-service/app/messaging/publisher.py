import json
import pika
from app.core.config import settings


class RabbitPublisher:
    def __init__(self):
        credentials = pika.PlainCredentials(
            settings.rabbitmq_user,
            settings.rabbitmq_password,
        )

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.rabbitmq_host,
                port=settings.rabbitmq_port,
                credentials=credentials,
            )
        )

        self.channel = self.connection.channel()

        self.channel.queue_declare(
            queue="speech_queue",
            durable=True,
        )

    def publish(
            self,
            file_id: int,
            object_name: str,
    ) -> None:
        message = {
            "file_id": file_id,
            "object_name": object_name,
        }

        self.channel.basic_publish(
            exchange="",
            routing_key="speech_queue",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
        )

    def close(self) -> None:
        if self.connection.is_open:
            self.connection.close()

