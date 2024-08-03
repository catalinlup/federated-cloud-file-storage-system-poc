from ..entities.event.Event import Event

class EventPublisher:
    """
    Defines the interface of an event publisher.
    """

    def publish_event(self, event: Event, queue_id: str):
        raise Exception('Not implemented')