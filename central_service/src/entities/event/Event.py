class Event:
    """
    Represents an event to be sent to one of the clients.
    """

    def __init__(self, event_id: str, event_unix_timestamp: int, event_type: str, content: dict) -> None:
        """
        Initializes an event object.
        """

        self.event_id = event_id
        self.event_unix_timestamp = event_unix_timestamp
        self.event_type = event_type
        self.content = content

    
    def to_json(self):
        """
        Converts this event to JSON.
        """

        return {
            'event_id': self.event_id,
            'event_unix_timestamp': self.event_unix_timestamp,
            'event_type': self.event_type,
            'content': self.content
        }

    
