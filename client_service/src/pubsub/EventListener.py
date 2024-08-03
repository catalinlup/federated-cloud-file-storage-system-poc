class EventListener:
    """
    Listens to events.
    """


    def on_event_received(self, queue_id: str, action):
        """
        Performs the provided action when a certain event is received.
        """
        raise Exception('Not implemented')
    
    def listen(self):
        raise Exception('Not implemented')
    
    def close(self):
        raise Exception('Not implemented')
    
    