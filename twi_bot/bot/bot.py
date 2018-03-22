# coding: utf-8
import math
import logging
import traceback

from twi_bot.bot.sensors import BaseSensor
from twi_bot.bot.acts import BaseAct
from twi_bot.bot.task import TaskParam

log = logging.getLogger(__name__)


class PatternError(Exception):
    pass


class PatternMath(object):
    """Встроенная библиотека математики"""
    sqrt = math.sqrt
    min = min
    max = max

    def __getattr__(self, item):
        raise PatternError('Функции "bot.math.%s" не существует' % item)


class PatternSensors(object):
    """Доступные датчики у бота"""

    def __init__(self):
        self._avalable = []

    def _add(self, p):
        assert isinstance(p, BaseSensor)
        if p.id in self._avalable:
            raise ValueError('Датчик с id="%s" уже подключен к боту' % p.id)
        self._avalable.append(p.id)
        self.__setattr__(p.id, p.value)

    def __getattr__(self, item):
        raise PatternError('Датчика "bot.sensors.%s" не существует' % item)


class PatternAct(object):
    """Доступные действия у бота"""

    def __init__(self):
        self._avalable = []
        self._selected = []

    def _add(self, p):
        assert isinstance(p, BaseAct)
        if p.id in self._avalable:
            raise ValueError('Действие с id="%s" уже добавлено к боту' % p.id)

        def func(weight):
            # сюда паттерны складывают предложенные варианты действий
            # self._selected.append((act, weight))
            self._selected.append((p.id, weight))  # todo для отладки пока так

        self.__setattr__(p.id, func)

    def __getattr__(self, item):
        raise PatternError('Действия "bot.act.%s" не существует' % item)


class PatternTaskParam(object):
    """Информация о текущей задаче"""

    def __init__(self, task_params=None):
        self._avalable = []
        if task_params:
            for i in task_params:
                self._add(i)

    def _add(self, p):
        assert isinstance(p, TaskParam)
        if p.id in self._avalable:
            raise ValueError('Параметр задачи с id="%s" уже добавлен к боту' % p.id)
        self._avalable.append(p.id)
        self.__setattr__(p.id, p.value)

    def __getattr__(self, item):
        raise PatternError('Параметра задачи "bot.task.%s" не существует' % item)


class Bot(object):
    math = PatternMath()

    def __init__(self):
        self.sensors = PatternSensors()
        self.act = PatternAct()
        self.task = PatternTaskParam()

    def add_sensor(self, sensor):
        # noinspection PyProtectedMember
        self.sensors._add(sensor)

    def add_act(self, act):
        # noinspection PyProtectedMember
        self.act._add(act)

    def make_desision(self, patterns, task_params=None):
        """

        :param patterns: запускаемые паттерны
        :param task_params:
        :return: список с предложенными вариантами действий (решения)
        """
        self.task = PatternTaskParam(task_params)

        for pattern in patterns:
            try:
                pattern(self)  # запускаем каждый паттерн
            except PatternError as e:
                log.error(e)
            except BaseException:
                log.fatal(traceback.format_exc())

        # noinspection PyProtectedMember
        result = self.act._selected
        self.act._selected = []
        return result
