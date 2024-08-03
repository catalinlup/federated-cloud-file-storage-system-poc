from .EventListener import EventListener
import pika

class RabbitMqEventListener(EventListener):
    """
    Listens to rabbit mq events.
    """

    def __init__(self, host: str, port: str, virtual_host: str, username: str, password: str):
        super().__init__()

        credentials = pika.PlainCredentials(username=username, password=password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host, credentials=credentials)
        )

        self.channel = self.connection.channel()


    def on_event_received(self, queue_id: str, action):
        """
        Configures an event handles for receiving events.
        """
        self.channel.queue_declare(queue=queue_id)
        self.channel.basic_consume(queue_id, on_message_callback=action, auto_ack=True)


    def listen(self):
        """
        Starts listening for events.
        """
        self.channel.start_consuming()

    def close(self):
        """
        Closes the connection"
        """
        self.connection.close()

    



    