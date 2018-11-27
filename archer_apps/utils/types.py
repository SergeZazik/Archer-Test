from enum import Enum


class ChoicesEnum(Enum):
    """
    Base class for django model field choices
    """
    @classmethod
    def choices(cls):
        return ((tag.name, tag.value) for tag in cls)
