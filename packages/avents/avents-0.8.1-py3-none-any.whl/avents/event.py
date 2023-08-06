from dataclasses import dataclass
from typing import Any


@dataclass
class Event:
    """
    A dataclass that defines an emitted event

    Attributes:
        name (str): The event name, used for parsing and listening for events
        content (Any): The content of the event, can contain anything
    """

    name: str
    content: Any

    def to_dict(self) -> dict:
        """

        Returns:
            A dictionary version of the object, received by vars()
        """
        return vars(self)
