import csv
import os
import random
import typing as t
from itertools import chain

from ankipoker.chips import CHIP_TYPES
from ankipoker.imagegen import image_key, create_image_for_chips
from ankipoker.types import BetType, ChipStack
from ankipoker.util import sum_chips, value_to_chips

OUTPUT_DIR = os.path.join('output', 'potodds')
IMAGE_DIR = os.path.join(OUTPUT_DIR, 'images')
OUT_FILE = os.path.join(OUTPUT_DIR, 'out.csv')
POT_MEAN = 3
POT_LAMBDA = 1 / POT_MEAN

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

if not os.path.exists(IMAGE_DIR):
    os.mkdir(IMAGE_DIR)

BET_TYPES = list(chain(
    [
        BetType('Large', lambda pv: (1 + random.expovariate(1 / 2)) * pv),
        BetType('2x Pot', lambda pv: 2 * pv),
        BetType('Pot', lambda pv: pv),
        BetType('Half-Pot', lambda pv: pv / 2),
        BetType('Quarter-Pot', lambda pv: pv / 4),
    ],
    [  # single chips
        BetType(f'Single {c.value}', lambda p, c=c: c.value)
        for c in CHIP_TYPES
        if c.value >= 1
    ],
))


def generate_pot() -> ChipStack:
    chips = dict()
    while (sum(chips.values())) < 1:
        chips = {
            c: min(20, int(random.expovariate(POT_LAMBDA * c.value)))
            for c in CHIP_TYPES
        }
    return chips


def generate_bet(pot_value: float) -> t.Tuple[ChipStack, str]:
    bet_fn = random.choice(BET_TYPES)
    bet_target_value = bet_fn.calc(pot_value)
    print(bet_fn.name, '|', bet_target_value)
    bet_in_chips = value_to_chips(bet_target_value)
    return bet_in_chips, bet_fn.name


def calc_pot_odds(pot: float, bet: float) -> float:
    return bet / (pot + 2 * bet)


image_cache = dict()


def get_image_for_chips(chips: ChipStack) -> str:
    key = image_key(chips)
    if key not in image_cache:
        image_cache[key] = create_image_for_chips(chips, supersample=4)
        image_cache[key].save(os.path.join(IMAGE_DIR, f'{key}.png'))
    return key


data = []

for i in range(100):
    pot = generate_pot()
    pv = sum_chips(pot)
    bet, bet_type = generate_bet(pv)
    bv = sum_chips(bet)
    po = calc_pot_odds(pv, bv)

    pot_image = get_image_for_chips(pot)
    bet_image = get_image_for_chips(bet)
    data.append([
        i,
        pv,
        bv,
        f'{po:.0%}',
        bet_type,
        f'<img src="{pot_image}.png">',
        f'<img src="{bet_image}.png">',
    ])
    print(data[-1])

with open(OUT_FILE, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(data)
