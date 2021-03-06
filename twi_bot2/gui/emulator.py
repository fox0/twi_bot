# coding: utf-8
import sys
import logging
import pygame

from twi_bot2.gui.sprites import GoalSprite, WallSprite, BotSprite
from twi_bot2.gui.dev import GoalDev, CoordXDev, CoordYDev

log = logging.getLogger(__name__)


def main():
    FPS = 60.0
    SIZE = 350, 350
    STEP = 20
    IS_SHOW_BACKGROUND = False

    pygame.init()
    pygame.display.set_caption('twi_bot 0.3.1 by fox')

    screen = pygame.display.set_mode(SIZE)
    background = pygame.Surface(SIZE)
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    all_sprites = pygame.sprite.Group()

    w = (
        (80, 120),
        (100, 120),
        (120, 120),
        (140, 120),
        (160, 120),
        (180, 120),
        (180, 140),
        (180, 160),
        (180, 180),
        (180, 200),
        (180, 220),
    )
    walls = pygame.sprite.Group()
    for x, y in w:
        walls.add(WallSprite(x, y, STEP))
    all_sprites.add(walls)

    goal = GoalSprite(280, 160, STEP / 2)
    all_sprites.add(goal)

    bot = BotSprite(walls, 91, 212, STEP / 2)
    bot.dev = [
        GoalDev('goal_x', 280),
        GoalDev('goal_y', 160),
        CoordXDev('coord_x'),
        CoordYDev('coord_y'),
        # MapDev()
    ]
    all_sprites.add(bot)

    bot2 = BotSprite(walls, 10, 10, STEP / 2)
    bot2.dev = [
        GoalDev('goal_x', 280),
        GoalDev('goal_y', 160),
        CoordXDev('coord_x'),
        CoordYDev('coord_y'),
    ]
    all_sprites.add(bot2)

    timer = pygame.time.Clock()
    while True:
        timer.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    sys.exit(0)

        all_sprites.update()

        if IS_SHOW_BACKGROUND:
            screen.blit(background, (0, 0))

        # сеточка
        color = 80, 80, 80
        for x in range(-5, SIZE[0], STEP):
            pygame.draw.line(screen, color, (x, 0), (x, SIZE[1]))
        for y in range(-5, SIZE[1], STEP):
            pygame.draw.line(screen, color, (0, y), (SIZE[1], y))

        for i in all_sprites:
            screen.blit(i.surf, i.rect)
        pygame.display.update()


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
        level=logging.DEBUG
    )
    main()
