# coding: utf-8
from twi_bot.simulator.common import get_fullpath
from twi_bot.simulator.sprites import Platform


def load_level(name):
    with open(get_fullpath(name)) as f:
        platforms = []
        x, y = 0, 0
        _, _, w, h = Platform(x, y).rect
        for row in f:
            for col in row:
                if col == '*':
                    platforms.append(Platform(x, y))
                x += w  # блоки платформы ставятся на ширине блоков
            y += h      # то же самое и с высотой
            x = 0
        return platforms
