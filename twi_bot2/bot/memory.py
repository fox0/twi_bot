# coding: utf-8

# todo local and global


class Node(object):
    """Узел графа"""

    def __init__(self):
        self.karma = 0
        self.scope = None
        self.l, self.r, self.u, self.d = None, None, None, None
