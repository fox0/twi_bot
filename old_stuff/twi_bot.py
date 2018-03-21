# coding: utf-8
"""
Фильтрация паттернов по битовой маске перед запуском
"""
import time
import random
import logging
from collections import namedtuple
import numpy as np
import pygame

log = logging.getLogger(__name__)

Vector_in = namedtuple('Vector_in', ['timestamp', 'z'])


class Drone(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.z = 0.0
        self.speed_z = 0.0
        self.prev_timestamp = time.time()
        self.rect = pygame.Rect(300, 0, 100, 10)
        self.image = pygame.image.load('simulator/data/platform.png')

    def get_vector_in(self):
        timestamp = time.time()
        self.z += self.speed_z * (timestamp - self.prev_timestamp)  # x = v*t
        self.rect.y = self.z
        self.prev_timestamp = timestamp
        return np.array(Vector_in(
            timestamp,
            self.z + random.randrange(-1, 1),
        ))

    def action_move_z(self, value):
        self.speed_z += value


class Pattern(object):
    def __init__(self, mask, is_active):
        self.mask = mask
        self.is_active = is_active
        self.prev_z = 0

    def run(self, vector_in, bot):  # todo
        z = vector_in[1]  # vector_in.z
        z_comm = 200
        delta = z - z_comm
        if abs(delta) > 2:
            force = delta * 2 + (z_comm - self.prev_z) * 1.5  # PID
            log.debug('%s', force)
            bot.action_move_z(-force)
            self.prev_z = z


def main():
    bot = Drone()
    rules = [
        Pattern(np.array(Vector_in(timestamp=False, z=True)), is_active=True),
    ]
    prev_vector_in = bot.get_vector_in()

    pygame.init()
    pygame.display.set_caption('0.1')
    screen = pygame.display.set_mode((800, 640))
    timer = pygame.time.Clock()
    while True:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return

        vector_in = bot.get_vector_in()
        # битовая маска. Какие из значений изменились.
        mask = (prev_vector_in - vector_in) != np.full_like(vector_in, 0.0)
        for rule in filter(lambda x: x.is_active, rules):
            # log.debug('%s & %s', mask, rule.mask)
            if (mask & rule.mask).any():
                # log.debug('выполнение паттерна')
                rule.run(vector_in, bot)
        log.info('z=%s', bot.z)

        screen.blit(bot.image, bot.rect)
        pygame.display.update()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
