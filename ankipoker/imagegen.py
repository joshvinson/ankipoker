from math import sqrt

from PIL import ImageDraw, Image, ImageFont, ImageColor

from ankipoker.types import ChipStack


def image_key(chips: ChipStack) -> str:
    return '_'.join(
        f'{count}x{c.value}'
        for c, count in sorted(chips.items(), key=lambda ci: ci[0].value)
        if count > 0
    )


def create_image_for_chips(
    chips: ChipStack,
    supersample: int = 1,
    max_count: int = 5
) -> Image:
    chips = {
        c: count for c, count in chips.items() if count > 0
    }
    chip_width = 100 * supersample
    padding = 2 * supersample
    chip_height = 25 * supersample
    desc_height = 40 * supersample

    outline_width = int(sqrt(chip_width * chip_height) / 20)

    max_chips = min(max_count, max(chips.values()))

    w = int(len(chips) * (chip_width + 2 * padding))
    h = int(2 * padding + (max_chips + 1) * chip_height + desc_height)

    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    font = ImageFont.truetype("arial.ttf", 20 * supersample)

    # for each chip type:
    for i, (c, count) in enumerate(sorted(
        chips.items(),
        key=lambda ci: ci[0].value
    )):
        if count > max_count:
            ecount = max_count
            overflow = True
        else:
            ecount = count
            overflow = False

        fill_color = c.color
        if sum(ImageColor.getrgb(fill_color)[:3]) < 128 * 3:
            outline_color = '#ccc'
        else:
            outline_color = '#444'

        x1 = padding + i * (chip_width + padding * 2)
        x2 = x1 + chip_width
        y1 = padding + (max_chips - ecount) * chip_height
        y2 = y1 + chip_height

        # fill
        d.ellipse([(x1, y1), (x2, y2)], fill_color, fill_color)
        d.ellipse(
            [
                (x1, y1 + ecount * chip_height),
                (x2, y2 + ecount * chip_height)
            ],
            fill_color, fill_color
        )
        d.rectangle(
            [
                (x1, y1 + chip_height / 2),
                (x2, y2 + ecount * chip_height - chip_height / 2)
            ],
            fill_color, fill_color
        )

        # top arc
        d.arc([(x1, y1), (x2, y2)], 0, 360, outline_color, outline_width)

        # each chip below arc
        for i in range(ecount):
            ix = (i + 1)
            y1b = y1 + chip_height * ix
            y2b = y2 + chip_height * ix
            d.arc([(x1, y1b), (x2, y2b)], 0, 180, outline_color, outline_width)

        # side lines
        y1s = y1 + chip_height / 2
        d.line(
            [(x1, y1s), (x1, y1s + ecount * chip_height)],
            outline_color,
            outline_width,
        )
        d.line(
            [(x2, y1s), (x2, y1s + ecount * chip_height)],
            outline_color,
            outline_width,
        )

        # text
        s = f'x{count}'
        sw, sh = d.textsize(s, font)

        x1t = x1 + chip_width / 2 - sw / 2
        y1t = y1s + (ecount + 1) * chip_height

        d.rectangle(
            [
                (x1t - 2 * padding, y1t - padding),
                (x1t + sw + padding, y1t + sh + 2 * padding),
            ],
            'white',
            'black',
            outline_width // 2,
        )
        d.text((x1t, y1t), s, 'black', font)

        if overflow:
            for i in range(1, ecount - 1):
                ix = (i + 1)
                y1b = y1 + chip_height * ix + chip_height / 4
                y2b = y2 + chip_height * ix - chip_height / 4
                ew = y2b - y1b
                x1b = x1 + chip_width / 2 - ew / 2
                x2b = x2 - chip_width / 2 + ew / 2
                d.ellipse([(x1b, y1b), (x2b, y2b)], outline_color,
                          outline_width)

    img = img.resize((w // supersample, h // supersample),
                     resample=Image.ANTIALIAS)

    return img
