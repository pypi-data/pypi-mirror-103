from enum import Enum
from enum import EnumMeta


class EventTypeMeta(EnumMeta):
    """
    A metaclass added to help with iteration of enum values
    """

    def __contains__(cls, item):
        """
        Allows iteration of an enum to see if a value exists like so:

        >>> class SomeEnum(Enum, metaclass=EventTypeMeta):
        >>>     some_element = 5
        >>>
        >>> print(5 in SomeEnum)
        >>> > True

        Args:
            item: Some elemt input for comparison

        Returns:
            A bool representing whether or not item is in the enum
        """
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEventType(Enum, metaclass=EventTypeMeta):
    """
    A base Enum type included that should be inherited to define listenable events outside of raw strings

    For example:

    >>> class MyEventType(BaseEventType):
    >>>     EVENT_1: str = "EVENT 1"
    >>>     EVENT_2: str = "EVENT 2"

    This is useful when passing into EventListener's listen decorator argument on which events to emit
    """

    def __str__(self):
        return self.value
