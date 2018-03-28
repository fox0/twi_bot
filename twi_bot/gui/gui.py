# coding: utf-8
import sys
import pygame
from twi_bot.gui.sprites import Bot, Wall, Goal


class GUI(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('twi_bot 0.2 by fox')

        self.screen = pygame.display.set_mode((300, 300))
        self.background = pygame.Surface((300, 300))
        self.background.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))

        self.all_sprites = pygame.sprite.Group()
        self.bot = Bot(10, 150)
        self.all_sprites.add(self.bot)

        self.goal = Goal(280, 150)
        self.all_sprites.add(self.goal)

        self.walls = pygame.sprite.Group()
        walls = (
            (180, 130),
            (180, 140),
            (180, 150),
            (180, 160),
            (180, 170),
        )
        for x, y in walls:
            self.walls.add(Wall(x, y))

        self.all_sprites.add(self.walls)

        self.timer = pygame.time.Clock()

    def update(self):
        self.timer.tick(10)
        self._exit()
        # self.screen.blit(self.background, (0, 0))
        for i in self.all_sprites:
            self.screen.blit(i.surf, i.rect)
        pygame.display.flip()

    @staticmethod
    def _exit():
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit()
