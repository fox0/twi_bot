# coding: utf-8
import logging
import pygame

from twi_bot2.kernel.pattern.load import get_patterns
from twi_bot2.gui.dev import Dev

log = logging.getLogger(__name__)


class AbstractSprite(pygame.sprite.Sprite):
    color = 0, 0, 0

    def __init__(self, x, y, size=10):
        super(AbstractSprite, self).__init__()
        self.surf = pygame.Surface((size, size))
        self.surf.fill(self.color)
        self.rect = pygame.Rect((x, y, size, size))


class WallSprite(AbstractSprite):
    color = 255, 0, 0


class GoalSprite(AbstractSprite):
    color = 0, 255, 0


class BotSprite(AbstractSprite):
    patterns = get_patterns(config_dir='../conf', cache_dir='../cache')

    # todo id

    def __init__(self, *args, **kwargs):
        super(BotSprite, self).__init__(*args, **kwargs)
        self.dev = []

    def update(self):
        # log.debug('update bot')
        dev = {}
        for i in self.dev:
            assert isinstance(i, Dev)
            dev[i.name] = i.read(self)  # todo

        acts = []
        for ls, pattern in self.patterns:
            kwargs = {}
            for i in ls:
                try:
                    kwargs[i] = dev[i]
                except KeyError:
                    log.error('unknown dev %s', i)
            log.debug('>>>%s, %s', pattern, kwargs)
            try:
                for act, w in pattern(**kwargs):
                    log.debug('<<<%s, %s', act, w)
                    acts.append((act, w))
            except BaseException as e:
                log.exception(e)

        if acts:
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
                log.error('unknown act %s', act)

        # todo pygame.sprite.collide_rect(self, p)
