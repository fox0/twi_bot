# coding: utf-8
import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Wall, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 0, 0))
        self.rect = pygame.Rect((x, y, 10, 10))


class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Goal, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((0, 255, 0))
        self.rect = pygame.Rect((x, y, 10, 10))


class Bot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bot, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((0, 0, 0))
        self.rect = pygame.Rect((x, y, 10, 10))  # todo 15, 15?
