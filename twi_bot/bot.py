# coding: utf-8
import math
import logging
from twi_bot.sensors import BaseSensor

log = logging.getLogger(__name__)


class PatternError(Exception):
    pass


class Math(object):
    """Встроенная библиотека математики"""
    sqrt = math.sqrt
    min = min
    max = max

    def __getattr__(self, item):
        raise PatternError('Функции "bot.math.%s" не существует' % item)


class Sensors(object):
    """Доступные датчики у бота"""

    def _add(self, sensor):
        assert isinstance(sensor, BaseSensor)
        try:
            self.__getattribute__(sensor.id)
            raise Exception('Датчик с id="%s" уже подключен к боту' % sensor.id)
        except AttributeError:
            self.__setattr__(sensor.id, sensor.value)

    def __getattr__(self, item):
        raise PatternError('Датчика "bot.sensors.%s" не существует' % item)


class Act(object):
    """Доступные действия у бота"""

    def __init__(self):
        self._selected_action = []

    def __getattr__(self, item):
        if item not in ['go_left', 'go_right', 'go_up', 'go_down']:  # todo
            raise PatternError('Действия "bot.act.%s" не существует' % item)

        def func(weight):
            # сюда паттерны складывают предложенные варианты действий
            self._selected_action.append((item, weight))

        return func


class Task(object):
    """Информация о текущей задаче"""

    def __getattr__(self, item):
        if item not in ['coord_x', 'coord_y']:  # todo
            raise PatternError('Параметра "bot.task.%s" не существует' % item)
        return 1


class Bot(object):
    math = Math()

    def __init__(self):
        # входные параметры
        self.sensors = Sensors()
        self.task = Task()

        # выходные
        self.act = Act()

    def add_sensor(self, sensor):
        # noinspection PyProtectedMember
        self.sensors._add(sensor)

    def make_desision(self, patterns):
        """

        :param patterns: запускаемые паттерны
        :return: список с предложенными вариантами действий (решения)
        """
        for pattern in patterns:
            try:
                pattern(self)  # запускаем каждый паттерн
            except PatternError as e:
                log.error(e)

        # noinspection PyProtectedMember
        result = self.act._selected_action
        self.act._selected_action = []
        return result
