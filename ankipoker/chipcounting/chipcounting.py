import csv
import os
import random
from math import sqrt

from ankipoker.chips import CHIP_TYPES
from ankipoker.imagegen import image_key, create_image_for_chips
from ankipoker.types import ChipStack
from ankipoker.util import sum_chips

OUTPUT_DIR = os.path.join('output', 'chipcounting')
IMAGE_DIR = os.path.join(OUTPUT_DIR, 'images')
OUT_FILE = os.path.join(OUTPUT_DIR, 'out.csv')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)


def generate_stack() -> ChipStack:
    chips = dict()
    while (sum(chips.values())) < 1:
        chips = {
            c: int(sqrt(random.expovariate(c.value / 10)))
            for c in CHIP_TYPES
        }
    return chips


image_cache = dict()


def get_image_for_chips(chips: ChipStack) -> str:
    key = image_key(chips)
    if key not in image_cache:
        image_cache[key] = create_image_for_chips(chips, supersample=4)
        image_cache[key].save(os.path.join(IMAGE_DIR, f'{key}.png'))
    return key


data = []

for i in range(1000):
    stack = generate_stack()
    value = sum_chips(stack)

    stack_image = get_image_for_chips(stack)
    data.append([
        i,
        f'${value:.2f}',
        f'<img src="{stack_image}.png">',
    ])
    print(data[-1], stack)

with open(OUT_FILE, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(data)
