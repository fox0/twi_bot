# coding: utf-8
import pygame

from old_stuff import load_level


class Simulator(object):
    def __init__(self):
        pass

    def add_bot(self):
        pass

    def run(self):
        pygame.init()
        pygame.display.set_caption('twi_simulator 0.1')
        screen = pygame.display.set_mode((800, 640))
        platforms = load_level('level.txt')

        timer = pygame.time.Clock()
        while True:
            timer.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        return

            for e in platforms:
                screen.blit(e.image, e.rect)
            pygame.display.update()


if __name__ == '__main__':
    Simulator().run()
