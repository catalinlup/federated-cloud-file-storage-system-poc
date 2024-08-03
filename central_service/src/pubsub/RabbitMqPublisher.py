from .EventPublisher import EventPublisher
from src.entities.event.Event import Event
import pika
import json
# from ..config_params import RABBIT_MQ_CONNECTION_STRING

class RabbitMqPublisher(EventPublisher):
    """
    Publishes an event to a rabbit mq topic.
    """

    def __init__(self, host: str, port: str, virtual_host: str, username: str, password: str) -> None:
        """

        """
        # credentials = pika.PlainCredentials(username='umfcyhuw', password='U0qZTAnvBfcWKtn1xbbIyjFXW3zY2ZIv')
        # self.connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='kangaroo.rmq.cloudamqp.com', port='5672', virtual_host='umfcyhuw', credentials=credentials)
        # )

        credentials = pika.PlainCredentials(username=username, password=password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host, credentials=credentials)
        )

        self.channel = self.connection.channel()

    def publish_event(self, event: Event, queue_id: str):
        self.channel.queue_declare(queue=queue_id)

        event_dict = event.to_json()
        event_str = json.dumps(event_dict)
        
        self.channel.basic_publish(exchange='', routing_key=queue_id, body=event_str)