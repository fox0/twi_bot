# coding: utf-8

# todo local and global


class Memory(object):
    def __init__(self, step):
        """

        :param step: шаг сетки, с какой детализацией данные хранятся в памяти
        """
        self.step = step
        self.__d = {}

    def get_node(self, x, y):
        """
        Вернуть узел графа или создать новый

        :param x, y: координаты, для которых запрашивается информация
        :return: объект Node
        """
        k = self.round(x), self.round(y)
        if k not in self.__d:
            self.__d[k] = Node(k)
        return self.__d[k]

    def round(self, v):
        """
        Из-за низкой детализации округляем координаты
        >>> m = Memory(20)
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


class Node(object):
    """Узел графа"""

    def __init__(self, xy):
        self.x, self.y = xy

        self.karma = 0
        self.scope = None  # todo список с timestamp

    def __str__(self):
        return '(%d;%d)' % (self.x, self.y)
