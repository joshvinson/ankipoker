from ankipoker.chips import CHIPS_BY_VALUE
from ankipoker.types import ChipStack


def value_to_chips(value: float) -> ChipStack:
    chips = dict()
    for cv, c in sorted(CHIPS_BY_VALUE.items(), key=lambda t: -t[0]):
        div = value // cv
        rem = value - (div * cv)
        if div > 0:
            chips[c] = int(div)
            value = rem

    return chips


def sum_chips(chips: ChipStack) -> float:
    return sum(c.value * count for c, count in chips.items())
