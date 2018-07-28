# coding: utf-8
import pygame
import logging


log = logging.getLogger(__name__)


class AbstractSprite(pygame.sprite.Sprite):
    color = 0, 0, 0

    def __init__(self, x, y, size=10):
        super(AbstractSprite, self).__init__()
        self.surf = pygame.Surface((size, size))
        self.surf.fill(self.color)
        self.rect = pygame.Rect((x, y, size, size))


class Bot(AbstractSprite):
    # todo id

    def update(self):
        log.debug('update bot')
        pass
        # step = 1
        # if command == 'go_right':
        #     self.bot.rect.x += step
        # elif command == 'go_left':
        #     self.bot.rect.x -= step
        # elif command == 'go_down':
        #     self.bot.rect.y += step
        # elif command == 'go_up':
        #     self.bot.rect.y -= step


class Wall(AbstractSprite):
    color = 255, 0, 0


class Goal(AbstractSprite):
    color = 0, 255, 0
