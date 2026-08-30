from app.consumer import RabbitConsumer


def main():
    consumer = RabbitConsumer()
    consumer.start()


if __name__ == "__main__":
    main()
