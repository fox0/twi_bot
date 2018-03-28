# coding: utf-8

# todo local and global


class Memory(object):
    def __init__(self):
        self.__d = {}

    def get_node(self, x, y):
        """
        Вернуть узел графа или создать новый

        :param x:
        :param y:
        :return:
        """
        k = x, y
        if k not in self.__d:
            self.__d[k] = Node(k)
        return self.__d[k]


class Node(object):
    """Узел графа"""

    def __init__(self, xy):
        self.x, self.y = xy

        self.karma = 0
        self.scope = None  # todo список с timestamp

    def __str__(self):
        return '(%d;%d)' % (self.x, self.y)
