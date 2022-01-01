from enum import Enum

"""A class that represents the colors."""


class Colors(Enum):
    WHITE = 0
    YELLOW = 1
    RED = 2

    @classmethod
    def tostring(cls, color):
        """Returns the string
        representation of a color."""
        if color == cls.WHITE:
            return "WHITE"
        elif color == cls.YELLOW:
            return "YELLOW"
        elif color == cls.RED:
            return "RED"
        else:
            return ValueError

    @classmethod
    def opposite(cls, color):
        """Returns the opposite
        color enumeration."""
        if color == cls.WHITE:
            return cls.WHITE
        elif color == cls.YELLOW:
            return cls.RED
        elif color == cls.RED:
            return cls.YELLOW
        else:
            return ValueError
