"""Holds classes related to interaction with the game back-end."""
from abc import ABC


class GameEvent(ABC):
    """Generic class for game events."""

    def __init__(self):
        """Construct the event."""
        pass


class MoveEvent(GameEvent):
    """Results for the move action."""

    def __init__(self, valid, promotion=False):
        """Construct the event.

        Parameters:
            valid(Bool): Was the move valid?

        Attributes:
            valid(Bool): Was the move valid?
        """
        self.valid = valid
        self.promotion = promotion

    def __bool__(self):
        """Bool representation."""
        return self.valid


class PromotionEvent(GameEvent):
    """Results for the promote action."""

    def __init__(self, valid):
        """Construct the event.

        Parameters:
            valid(Bool): Was the promotion valid?

        Attributes:
            valid(Bool): Was the promotion valid?
        """
        self.valid = valid

    def __bool__(self):
        """Bool representation."""
        return self.valid
