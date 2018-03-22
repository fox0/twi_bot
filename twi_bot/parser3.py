#!/usr/bin/env python2
# coding: utf-8
import math
import logging
from twi_bot.compile import load_pattern, PatternError

log = logging.getLogger(__name__)


class Sensors(object):
    """Доступные датчики у бота"""

    def __getattr__(self, item):
        if item not in ['wall_l', 'wall_r', 'wall_u', 'wall_d', 'coord_x', 'coord_y']:  # todo
            raise PatternError('Датчика "bot.sensors.%s" не существует' % item)
        if item == 'wall_r':  # todo
            return 4
        return 10


class Act(object):
    """Доступные действия у бота"""

    def __getattr__(self, item):
        if item not in ['go_left', 'go_right', 'go_up', 'go_down']:  # todo
            raise PatternError('Действия "bot.act.%s" не существует' % item)

        def func(weight):
            print(item, weight)  # todo

        return func


class Task(object):
    """Информация о текущей задаче"""

    def __getattr__(self, item):
        if item not in ['coord_x', 'coord_y']:  # todo
            raise PatternError('Параметра "bot.task.%s" не существует' % item)
        return 1


class Bot(object):
    """Сам бот"""

    class math(object):
        """Встроенная библиотека математики"""
        sqrt = math.sqrt
        min = min
        max = max

        def __getattr__(self, item):
            raise PatternError('Функции "bot.math.%s" не существует' % item)

    def __init__(self):
        # входные параметры
        self.sensors = Sensors()
        self.task = Task()

        # выходные
        self.act = Act()


def main():
    # pattern = load_pattern('patterns/example1.conf')
    pattern = load_pattern('patterns/example2.conf')
    bot = Bot()
    pattern(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )
    main()
