class EventBus:
    _subscribers = {}

    @classmethod
    def subscribe(cls, event_name, callback):
        """Register a callback for a specific event."""
        if event_name not in cls._subscribers:
            cls._subscribers[event_name] = []
        cls._subscribers[event_name].append(callback)

    @classmethod
    def send(cls, event_name, data=None):
        """Trigger an event and notify all subscribers."""
        if event_name in cls._subscribers:
            for callback in cls._subscribers[event_name]:
                callback(data)

def send_message(event_name, message):
    print(f"Sent {event_name} message {message} to all subscribers")
    EventBus.send(event_name, message)

def subscribe_event(event_name, callback):
    EventBus.subscribe(event_name, callback)