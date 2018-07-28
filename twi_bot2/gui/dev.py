# coding: utf-8
"""Эмулируемые устройства"""


class Dev(object):
    def __init__(self, name):
        self.name = name

    def read(self, bot):  # todo
        raise NotImplementedError

    def write(self, value):
        raise NotImplementedError


class DevRead(Dev):
    """Устройство read only"""
    def read(self, bot):
        raise NotImplementedError

    def write(self, value):
        pass


class GoalDev(DevRead):
    def __init__(self, name, value):
        super(GoalDev, self).__init__(name)
        self.value = value

    def read(self, bot):
        return self.value


class CoordXDev(DevRead):
    """Координаты роботв X"""
    def read(self, bot):
        return bot.rect.x


class CoordYDev(DevRead):
    """Координаты роботв Y"""
    def read(self, bot):
        return bot.rect.y


class MapDev(DevRead):
    def __init__(self, step, *args, **kwargs):
        self.step = step
        self.d = {}
        super(MapDev, self).__init__(*args, **kwargs)

    def read(self, bot):  # todo читать пару координат XY
        return bot.rect.y

    def round(self, v):
        """
        Из-за низкой детализации округляем координаты

        >>> m = MapDev(20)
        >>> m.round(9)
        0
        >>> m.round(10)
        0
        >>> m.round(11)
        20
        >>> m.round(19)
        20
        >>> m.round(20)
        20
        >>> m.round(30)
        20
        >>> m.round(40)
        40
        """
        if v % self.step == 0:
            return v
        for i in range(self.step / 2 + 1):
            v1 = v - i
            if v1 % self.step == 0:
                return v1
            v1 = v + i
            if v1 % self.step == 0:
                return v1
        raise ValueError
