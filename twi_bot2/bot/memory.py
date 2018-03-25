# coding: utf-8

# todo local and global


class Node(object):
    """Узел графа"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.karma = 0
        self.scope = None

    def __str__(self):
        return '(%d;%d)' % (self.x, self.y)
