"""time unit enum"""
from enum import Enum


class TimeUnitEnum(Enum):
    """enum to handle time unit"""
    DAYS = 'DAYS'
    HOURS = 'HOURS'
    MINUTES = 'MINUTES'
    SECONDS = 'SECONDS'

    @classmethod
    def has_value(cls, value: str):
        """true if the value is in the enum else false"""
        return value.upper() in TimeUnitEnum.__members__
