from ankipoker.types import ChipType

CHIP_TYPES = [
    ChipType(0.25, '#ddd'),
    ChipType(0.5, '#c33'),
    ChipType(1, '#33c'),
    ChipType(5, '#393'),
    ChipType(20, '#333'),
]

CHIPS_BY_VALUE = {
    c.value: c for c in CHIP_TYPES
}
