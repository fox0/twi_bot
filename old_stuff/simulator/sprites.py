# coding: utf-8
import pygame

from old_stuff import get_fullpath


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('platform.png')
        _, _, w, h = self.image.get_rect()
        self.rect = pygame.Rect(x, y, w, h)


def load_image(name):
    image = pygame.image.load(get_fullpath(name))
    return image.convert_alpha() if image.get_alpha() else image.convert()
