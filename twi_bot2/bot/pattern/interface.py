# coding: utf-8
"""
Единственный интерфейс для передачи данных к/от паттерна.

В коде паттерна доступна глобальная переменная bot.

* bot.math - библиотека математических функций
* ...
"""
# todo doc
import math


class RunTimePatternError(Exception):
    pass


class PatternInterfaceMath(object):
    """Встроенная библиотека математики"""
    sqrt = math.sqrt
    min = min
    max = max

    def __getattr__(self, item):
        raise RunTimePatternError('Функции "bot.math.%s" не существует' % item)


class PatternInterfaceSensors(object):
    def __init__(self, avalable):
        self._dict = avalable

    def __getattr__(self, item):
        try:
            return self._dict[item]
        except KeyError:
            raise RunTimePatternError('Датчика "bot.sensors.%s" не существует' % item)


class PatternInterfaceTaskParam(object):
    def __init__(self, task_params):
        self._dict = task_params

    def __getattr__(self, item):
        try:
            return self._dict[item]
        except KeyError:
            raise RunTimePatternError('Параметра задачи "bot.task.%s" не существует' % item)


class PatternInterfaceAct(object):
    def __init__(self, acts):
        self._list = acts
        self._selected = []

    def __getattr__(self, item):
        if item not in self._list:
            raise RunTimePatternError('Действия "bot.act.%s" не существует' % item)

        def func(weight):
            self._selected.append((item, weight))

        return func


class PatternInterfaceBot(object):
    math = PatternInterfaceMath()

    def __init__(self, sensors, acts, task_params=None):
        self.sensors = PatternInterfaceSensors(sensors)
        self.task = PatternInterfaceTaskParam(task_params or {})
        self.act = PatternInterfaceAct(acts)

    def __getattr__(self, item):
        raise RunTimePatternError('"bot.%s" не существует' % item)
