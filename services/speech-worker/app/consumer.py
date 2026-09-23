import asyncio
import json
import os

import pika

from app.config import settings
from app.db.session import async_session_factory
from app.repositories.transcription_repository import TranscriptionRepository
from app.repositories.file_repository import FileRepository
from app.services.transcription_service import TranscriptionService
from app.storage.service import StorageService


class RabbitConsumer:
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

        self.storage = StorageService()
        self.transcription_service = TranscriptionService()

    async def update_file_status(
        self,
        file_id: int,
        status: str,
    ):
        async with async_session_factory() as session:
            repository = FileRepository(session)

            file = await repository.update_status(
                file_id=file_id,
                status=status,
            )

            if file is None:
                raise ValueError(
                    f"Audio file not found: {file_id}"
                )

            return file

    async def save_transcription(
        self,
        file_id: int,
        text: str,
        language: str,
    ):
        async with async_session_factory() as session:
            repository = TranscriptionRepository(session)

            transcription = await repository.create(
                file_id=file_id,
                text=text,
                language=language,
            )

            return transcription

    def callback(self, ch, method, properties, body):
        message = json.loads(body)

        file_id = message["file_id"]
        object_name = message["object_name"]

        destination = f"/tmp/{object_name}"

        print("Received message:")
        print(message)

        try:
            # Mark file as processing immediately
            asyncio.run(
                self.update_file_status(
                    file_id=file_id,
                    status="processing",
                )
            )

            print("File status: processing")

            # 1. Download audio from MinIO
            self.storage.download_file(
                object_name=object_name,
                destination=destination,
            )

            print(f"File downloaded: {destination}")
            print(f"File exists: {os.path.exists(destination)}")

            # 2. Transcribe audio with Faster-Whisper
            print("Starting transcription...")

            result = self.transcription_service.transcribe(
                destination,
            )

            text = result["text"]
            language = result["language"]

            print(f"Language detected: {language}")
            print(f"Transcription: {text}")

            # 3. Save transcription to PostgreSQL
            transcription = asyncio.run(
                self.save_transcription(
                    file_id=file_id,
                    text=text,
                    language=language,
                )
            )

            print(
                f"Transcription created: "
                f"id={transcription.id}, "
                f"file_id={transcription.file_id}"
            )

            # Mark file as completed
            asyncio.run(
                self.update_file_status(
                    file_id=file_id,
                    status="completed",
                )
            )

            print("File status: completed")

            # 4. Acknowledge RabbitMQ message
            ch.basic_ack(
                delivery_tag=method.delivery_tag,
            )

            print("Message acknowledged.")

        except Exception as exc:
            print(f"Error processing message: {exc}")

            try:
                asyncio.run(
                    self.update_file_status(
                        file_id=file_id,
                        status="failed",
                    )
                )

                print("File status: failed")

            except Exception as status_exc:
                print(
                    f"Failed to update file status: "
                    f"{status_exc}"
                )

            # Do not acknowledge failed message.
            # Requeue it so RabbitMQ can deliver it again.
            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=True,
            )

            print("Message rejected and requeued.")

        finally:
            # Remove temporary downloaded audio file
            if os.path.exists(destination):
                os.remove(destination)
                print(f"Temporary file removed: {destination}")

    def start(self):
        self.channel.basic_consume(
            queue="speech_queue",
            on_message_callback=self.callback,
        )

        print("Speech Worker started.")
        print("Waiting for messages...")

        self.channel.start_consuming()