#!/usr/bin/env python2
# coding: utf-8
import logging
import pygame

from twi_bot.bot.bot import Bot
from twi_bot.main import get_patterns, make_desision1

log = logging.getLogger(__name__)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((0, 0, 0))
        self.rect = pygame.Rect((x, y, 0, 0))

        self.bot = Bot()
        self.patterns = get_patterns()

    def update(self):
        # command, _ = make_desision1(self.bot, self.patterns)

        self.rect.x += 1


def main():
    pygame.init()
    pygame.display.set_caption('twi_bot 0.1 by fox')
    screen = pygame.display.set_mode((300, 300))

    background = pygame.Surface((300, 300))
    background.fill((255, 255, 255))

    player = Player(10, 100)

    timer = pygame.time.Clock()
    while True:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return

        player.update()

        screen.blit(background, (0, 0))
        screen.blit(player.surf, player.rect)
        pygame.display.flip()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )
    main()
