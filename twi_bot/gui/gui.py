# coding: utf-8
import sys
import pygame
from twi_bot.gui.sprites import Bot, Wall, Goal


class GUI(object):
    SIZE = 600, 600

    def __init__(self, step, xy_bot, xy_goal, walls):
        """

        :param step: шаг сетки
        :param xy_bot:
        :param xy_goal:
        :param walls:
        :return:
        """
        pygame.init()
        pygame.display.set_caption('twi_bot 0.2.1 by fox')

        self.screen = pygame.display.set_mode(self.SIZE)
        self.background = pygame.Surface(self.SIZE)
        self.background.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))

        self.all_sprites = pygame.sprite.Group()

        self.goal = Goal(xy_goal[0], xy_goal[1], step)
        self.all_sprites.add(self.goal)

        self.walls = pygame.sprite.Group()
        for x, y in walls:
            self.walls.add(Wall(x, y, step))
        self.all_sprites.add(self.walls)

        self.bot = Bot(xy_bot[0], xy_bot[1], step / 2)
        self.all_sprites.add(self.bot)

        self.timer = pygame.time.Clock()
        self.step = step

    def update(self, tick=10, is_show_background=False):
        self.timer.tick(tick)
        self._exit()

        if is_show_background:
            self.screen.blit(self.background, (0, 0))

        # сеточка
        color = 80, 80, 80
        for x in range(0, self.SIZE[0], self.step):
            pygame.draw.line(self.screen, color, (x, 0), (x, self.SIZE[1]))
        for y in range(0, self.SIZE[1], self.step):
            pygame.draw.line(self.screen, color, (0, y), (self.SIZE[1], y))

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

    def get_sensors(self):
        step = self.step - 7
        sensors = {
            'wall_l': 10,
            'wall_r': 10,
            'wall_u': 10,
            'wall_d': 10,
            'coord_x': self.bot.rect.centerx,
            'coord_y': self.bot.rect.centery,
        }
        for wall in self.walls:
            if wall.rect.collidepoint(self.bot.rect.x + step, self.bot.rect.y):
                sensors['wall_r'] = 0
            if wall.rect.collidepoint(self.bot.rect.x - step, self.bot.rect.y):
                sensors['wall_l'] = 0
            if wall.rect.collidepoint(self.bot.rect.x, self.bot.rect.y + step):
                sensors['wall_d'] = 0
            if wall.rect.collidepoint(self.bot.rect.x, self.bot.rect.y - step):
                sensors['wall_u'] = 0
        return sensors

    def execute_command(self, command):
        step = 1
        if command == 'go_right':
            self.bot.rect.x += step
        elif command == 'go_left':
            self.bot.rect.x -= step
        elif command == 'go_down':
            self.bot.rect.y += step
        elif command == 'go_up':
            self.bot.rect.y -= step
        else:
            raise NotImplementedError
