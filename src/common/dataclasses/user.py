# from fractions import Fraction
from pydantic.dataclasses import dataclass


@dataclass
class UserTime:
    slot_count: str
    slot_empty: str
    last_updated_timestamp: float
    interval: float
    speed_count: int
