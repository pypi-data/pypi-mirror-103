import asyncio
from avents.event import Event


class EventListener:
    """
    A class that implements a listen decorator and parser.

    Can be inherited from to generate custom listeners like so:

    >>> class CustomListener(EventListener):
    >>>     ...

    A constructor is not necessary on child classes, but you can still do the following:

    >>> class CustomListener(EventListener):
    >>>     def __init__(self):
    >>>         super().__init__()

    Inheriting EventListener to create a custom listener allows sub parsing of events, for example:

    >>> class CustomListener(EventListener):
    >>>     ...
    >>>
    >>>
    >>> @EventListener.listen("BASE EVENT")
    >>> async def base_event_handler(event: Event):
    >>>     # Where event.content contains a dict defining another event class, e.g.
    >>>     # {
    >>>     #   "name": "EVENT NAME",
    >>>     #   "content" "some event content"
    >>>     # }
    >>>     await CustomListener.parse(Event(**event.content))
    >>>
    >>> @CustomListener.listen("EVENT NAME")
    >>> async def some_custom_event(event: Event):
    >>>     print(event.content)
    """

    def __init__(self):
        """This allows this class to be inheritable to extend events to other classes"""
        cls = self.__class__

        try:
            _listening_events = getattr(cls, "_listening_events")
            if not _listening_events.get(cls):
                _listening_events[cls] = {}

        except AttributeError:
            setattr(cls, "_listening_events", {})

    @classmethod
    def listen(cls, *events: str):
        """
        A decorator that can be used to wrap coroutines (async functions) such that they listen for event emissions

        This registers each listening coroutine to the listeners parent class

        For example:

        >>> @EventListener.listen("some event")
        >>> async def some_event(event: Event):
        >>>     print(event)

        Listen can also handle multiple events:

        >>> @EventListener.listen("some event", "another event", "yet another event")
        >>> async def event_listener(event: Event):
        >>>     print(event)

        Args:
            event (str): The name of the event (the first argument passed to the Event class)

        Returns:
            The decorator wrap
        """
        def decorator(function):
            for event in events:
                event = str(event)
                _listening_events: dict = cls().__getattribute__("_listening_events")


                if not _listening_events[cls].get(event):
                    _listening_events[cls][event] = []
                _listening_events[cls][event].append(function)

        return decorator

    @classmethod
    async def parse(cls, event: Event):
        """
        A coroutine that is used to parse events

        For Example:

        >>> async def some_func():
        >>>     for i in range(2):
        >>>         await EventListener().parse(Event(name=str(i), content=f"Content-{i}"))

        This would call functions wrapped with the listen decorator for each proper event name

        Args:
            event (Event): An object defining events to be emitted to listening coroutines
        """
        _listening_events: dict = cls().__getattribute__("_listening_events")

        if events := _listening_events[cls].get(event.name, None):
            tasks = []
            for listener in events:
                tasks.append(listener(event))
            await asyncio.gather(*tasks)
