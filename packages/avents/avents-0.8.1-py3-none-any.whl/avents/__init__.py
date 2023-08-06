"""
Basic Usage:

>>> from avents import parse
>>> from avents import listen
>>> from avents import Event
>>>
>>> async def some_event_emitter():
>>>     await parse(Event("event", "content"))
>>>
>>> @listen("event")
>>> async def some_listener(event: Event):
>>>     print(event)
>>>

Advanced Usage:

>>> from avents import parse
>>> from avents import listen
>>> from avents import Event
>>> from avents import EventListener
>>> from avents import BaseEventType
>>>
>>>
>>> class CustomEventType(BaseEventType):
>>>     CUSTOM_EVENT: str = "custom event"
>>>     SUB_EVENT: str = "sub event"
>>>
>>>
>>> class CustomListener(EventListener):
>>>     ...
>>>
>>>
>>> async def example_event_emitter():
>>>     await parse(Event("custom event",
>>>             {"name": "sub event",
>>>              "content": "sub event content"})
>>>     )
>>>
>>> @listen(CustomEventType.CUSTOM_EVENT)
>>> async def base_parser(emitted_event: Event):
>>>     await CustomListener.parse(Event(**emitted_event.content))
>>>
>>> @CustomListener.listen(CustomEventType.SUB_EVENT)
>>> async def sub_parser(sub_event: Event):
>>>     print(sub_event)
>>>

"""

from avents.listener import EventListener
from avents.type import BaseEventType
from avents.event import Event

listen = EventListener().listen
parse = EventListener().parse

__all__ = [
    "listen",
    "parse",
    "EventListener",
    "BaseEventType",
    "Event"
]
