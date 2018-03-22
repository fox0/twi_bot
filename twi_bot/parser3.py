#!/usr/bin/env python2
# coding: utf-8
import logging
from twi_bot.compile import load_pattern, PatternError

log = logging.getLogger(__name__)


class Sensors(object):
    def __getattr__(self, item):
        if item not in ['wall_l', 'wall_r', 'wall_u', 'wall_d']:  # todo
            raise PatternError('Датчика "%s" не существует' % item)
        if item == 'wall_r':  # todo
            return 4
        return 10


class Act(object):
    def __getattr__(self, item):
        if item not in ['go_left', 'go_right', 'go_up', 'go_down']:  # todo
            raise PatternError('Действия "%s" не существует' % item)

        def func(weight):
            print(item, weight)  # todo

        return func


class Bot(object):
    def __init__(self):
        self.sensors = Sensors()
        self.act = Act()


def main():
    pattern = load_pattern('patterns/example1.conf')
    bot = Bot()
    pattern(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )
    main()
