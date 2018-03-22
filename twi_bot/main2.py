#!/usr/bin/env python2
# coding: utf-8
import logging
import pygame

from twi_bot.bot.bot import Bot
from twi_bot.bot.acts import BaseAct
from twi_bot.bot.sensors import BaseSensor
from twi_bot.bot.task import TaskParam
from twi_bot.main import get_patterns, make_desision1

log = logging.getLogger(__name__)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, coord_goal):
        super(Player, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((0, 0, 0))
        self.rect = pygame.Rect((x, y, 10, 10))

        self.bot = Bot()
        self.bot.add_act(BaseAct('go_left'))
        self.bot.add_act(BaseAct('go_up'))
        self.bot.add_act(BaseAct('go_right'))
        self.bot.add_act(BaseAct('go_down'))
        self.patterns = get_patterns()
        self.coord_goal = coord_goal

    def update(self, walls):
        # грязный хак
        self.bot.sensors._avalable = []
        d = 100
        for i in walls:
            if self.rect.colliderect(i.rect):
                self.rect.x -= 1
                d = 0
        self.bot.sensors._add(Sensor('wall_l', 100))
        self.bot.sensors._add(Sensor('wall_r', d))
        self.bot.sensors._add(Sensor('wall_u', 100))
        self.bot.sensors._add(Sensor('wall_d', 100))
        self.bot.sensors._add(Sensor('coord_x', self.rect.x))
        self.bot.sensors._add(Sensor('coord_y', self.rect.y))

        task_params = [
            Param('coord_x', self.coord_goal[0]),
            Param('coord_y', self.coord_goal[1]),
        ]
        command, _ = make_desision1(self.bot, self.patterns, task_params)
        if command == 'go_right':
            self.rect.x += 1
        elif command == 'go_left':
            self.rect.x -= 1
        elif command == 'go_down':
            self.rect.y += 1
        elif command == 'go_up':
            self.rect.y -= 1
        else:
            raise NotImplementedError
        log.debug('x=%d, y=%d', self.rect.x, self.rect.y)


class Sensor(BaseSensor):
    def __init__(self, name_id, value):
        super(Sensor, self).__init__(name_id)
        self.value = value


class Param(TaskParam):
    def __init__(self, name_id, value):
        super(Param, self).__init__(name_id)
        self.value = value


class Goal(pygame.sprite.Sprite):
    def __init__(self, coord_goal):
        super(Goal, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((0, 255, 0))
        self.rect = pygame.Rect((coord_goal[0], coord_goal[1], 10, 10))


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Wall, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 0, 0))
        self.rect = pygame.Rect((x, y, 10, 10))


def main():
    pygame.init()
    pygame.display.set_caption('twi_bot 0.1 by fox')
    screen = pygame.display.set_mode((300, 300))

    background = pygame.Surface((300, 300))
    background.fill((255, 255, 255))

    # all_sprites = pygame.sprite.Group()

    coord_goal = (280, 100)
    player = Player(10, 200, coord_goal)
    goal = Goal(coord_goal)

    walls = pygame.sprite.Group()
    walls.add(Wall(200, 100))

    timer = pygame.time.Clock()
    while True:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return

        player.update(walls)

        screen.blit(background, (0, 0))
        for i in walls:
            screen.blit(i.surf, i.rect)
        screen.blit(goal.surf, goal.rect)
        screen.blit(player.surf, player.rect)
        pygame.display.flip()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )
    main()
