# coding: utf-8
import math
from twi_bot.sensors import BaseSensor


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

    def _reset_selected_action(self):
        self._selected_action = []

    def __getattr__(self, item):
        if item not in ['go_left', 'go_right', 'go_up', 'go_down']:  # todo
            raise PatternError('Действия "bot.act.%s" не существует' % item)

        def func(weight):
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
