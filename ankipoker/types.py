import typing as t
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class BetType:
    name: str
    calc: t.Callable[[float], float]


@dataclass(frozen=True, eq=True)
class ChipType:
    value: float
    color: str


ChipStack = t.Dict[ChipType, int]
