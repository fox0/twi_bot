# coding: utf-8
import pygame
import logging
from twi_bot2.kernel.pattern.load import get_patterns

log = logging.getLogger(__name__)


class AbstractSprite(pygame.sprite.Sprite):
    color = 0, 0, 0

    def __init__(self, x, y, size=10):
        super(AbstractSprite, self).__init__()
        self.surf = pygame.Surface((size, size))
        self.surf.fill(self.color)
        self.rect = pygame.Rect((x, y, size, size))


class Wall(AbstractSprite):
    color = 255, 0, 0


class Goal(AbstractSprite):
    color = 0, 255, 0


class Bot(AbstractSprite):
    patterns = get_patterns(config_dir='../conf', cache_dir='../cache')

    # todo id

    def update(self):
        # log.debug('update bot')
        dev = {
            'coord_x': self.rect.x,
            'coord_y': self.rect.y,
            'goal_x': 280,  # todo
            'goal_y': 160,
        }

        acts = []
        for ls, pattern in self.patterns:
            kwargs = {}
            for i in ls:
                kwargs[i] = dev[i]
            log.debug('>>>%s, %s', pattern, kwargs)
            try:
                for act, w in pattern(**kwargs):
                    log.debug('<<<%s, %s', act, w)
                    acts.append((act, w))
            except BaseException as e:
                log.exception(e)

        # todo sum
        step = 1
        act = sorted(acts, key=lambda x: -x[1])[0][0]
        log.debug('act=%s', act)
        if act == 'go_right':
            self.rect.x += step
        elif act == 'go_left':
            self.rect.x -= step
        elif act == 'go_down':
            self.rect.y += step
        elif act == 'go_up':
            self.rect.y -= step
        else:
            log.error('act=%s', act)
