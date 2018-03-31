# coding: utf-8
import logging

import matplotlib.pyplot as plt
import networkx as nx

log = logging.getLogger(__name__)


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
        k = self.round(x) / self.step, self.round(y) / self.step
        if k not in self.__d:
            self.__d[k] = Node(k[0], k[1])
        result = self.__d[k]
        assert isinstance(result, Node)
        return result

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

    def show_graph(self):
        """"Визуализировать граф"""
        graph = nx.Graph()
        for node in self.__d.values():
            # log.debug('node %s scope=%s', node, node.scope)
            graph.add_node(node)
            for node2 in node.edges:
                graph.add_edge(node, node2)

        pos = {}
        for node in graph.nodes():
            pos[node] = node.x, -node.y

        shape = {}
        for node in graph.nodes():
            k = 's' if node.scope else 'o'
            shape.setdefault(k, []).append(node)

        for node_shape, nodelist in shape.items():
            node_color = _get_color_nodes(nodelist)
            nx.draw_networkx_nodes(graph, pos, node_shape=node_shape, node_color=node_color, nodelist=nodelist)
        nx.draw_networkx_edges(graph, pos)
        plt.show()


def _get_color_nodes(nodes):
    node_color = [node.scope for node in nodes]
    ls = [i for i in node_color if i]
    if not ls:
        return 1, 1, 1
    max_scope = max(ls)
    node_color = [i / max_scope if i else 1 for i in node_color]
    return [(i, i, i) for i in node_color]


class Node(object):
    """Узел графа"""

    def __init__(self, x, y):
        self.x, self.y = x, y

        # указатели на соседей
        self.edges = set()

        self.karma = 0
        self.scope = None  # todo список с timestamp

    def add_link(self, node):
        """Добавить к ноде соседа"""
        assert isinstance(node, Node)
        if node == self:
            return
        self.edges.add(node)
        node.edges.add(self)

    def __str__(self):
        return '(%d;%d)' % (self.x, self.y)
