# coding: utf-8
import pygame


class AbstractSprite(pygame.sprite.Sprite):
    color = 0, 0, 0

    def __init__(self, x, y, size=10):
        super(AbstractSprite, self).__init__()
        self.surf = pygame.Surface((size, size))
        self.surf.fill(self.color)
        self.rect = pygame.Rect((x, y, size, size))


class Bot(AbstractSprite):
    pass


class Wall(AbstractSprite):
    color = 255, 0, 0


class Goal(AbstractSprite):
    color = 0, 255, 0
