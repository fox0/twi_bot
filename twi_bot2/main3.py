#!/usr/bin/env python2
# coding: utf-8
import logging
import traceback

import matplotlib.pyplot as plt
import networkx as nx

from twi_bot2.bot.pattern.load import load_patterns
from twi_bot2.bot.pattern.interface import PatternInterfaceBot, RunTimePatternError
from twi_bot2.bot.memory import Node
from twi_bot2.gui.gui import GUI

log = logging.getLogger(__name__)

avalable_acts = ['go_left', 'go_right', 'go_down', 'go_up']


def main():
    graph = nx.Graph()
    gui = GUI()
    step = 10

    memory = {}

    # todo выбор задачи
    patterns = load_patterns()
    for _ in range(20):
        sensors = {
            'wall_l': 10,
            'wall_r': 10,
            'wall_u': 10,
            'wall_d': 10,
            'coord_x': gui.bot.rect.x,
            'coord_y': gui.bot.rect.y,
        }
        for wall in gui.walls:
            if wall.rect.collidepoint(gui.bot.rect.x + step, gui.bot.rect.y):
                sensors['wall_r'] = 0
            if wall.rect.collidepoint(gui.bot.rect.x - step, gui.bot.rect.y):
                sensors['wall_l'] = 0
            if wall.rect.collidepoint(gui.bot.rect.x, gui.bot.rect.y + step):
                sensors['wall_d'] = 0
            if wall.rect.collidepoint(gui.bot.rect.x, gui.bot.rect.y - step):
                sensors['wall_u'] = 0

        task_params = {
            'coord_x': gui.goal.rect.x,
            'coord_y': gui.goal.rect.y,
        }
        bot = PatternInterfaceBot(sensors, avalable_acts, task_params)

        def add_node(x, y):
            if (x, y) not in memory:
                memory[(x, y)] = Node(x, y)
            return memory[(x, y)]

        prev_node = add_node(gui.bot.rect.x, gui.bot.rect.y)

        acts3 = get_command(bot, patterns)
        for command, _ in acts3:
            if command == 'go_right':
                node = add_node(gui.bot.rect.x + step, gui.bot.rect.y)
            elif command == 'go_left':
                node = add_node(gui.bot.rect.x - step, gui.bot.rect.y)
            elif command == 'go_down':
                node = add_node(gui.bot.rect.x, gui.bot.rect.y + step)
            elif command == 'go_up':
                node = add_node(gui.bot.rect.x, gui.bot.rect.y - step)
            else:
                raise NotImplementedError
            graph.add_edge(prev_node, node)

        command = acts3[0][0]
        log.info('Принято решение выполнить действие "%s"', command)

        if command == 'go_right':
            gui.bot.rect.x += step
        elif command == 'go_left':
            gui.bot.rect.x -= step
        elif command == 'go_down':
            gui.bot.rect.y += step
        elif command == 'go_up':
            gui.bot.rect.y -= step
        else:
            raise NotImplementedError
        gui.update()

    nx.draw_networkx(graph)
    plt.show()


def get_command(bot, patterns):
    for pattern in patterns:
        try:
            pattern(bot)
        except RunTimePatternError as e:
            log.error(e)
        except BaseException:
            log.critical(traceback.format_exc())
    # noinspection PyProtectedMember
    return make_desision1(bot.act._selected)


def make_desision1(acts):
    log.debug('acts=%s', acts)
    acts2 = sum_result(acts)
    log.info(acts2)
    acts3 = filter(lambda x: x[1] > 0, acts2)
    log.info(acts3)
    return acts3


def sum_result(acts):
    d = {}
    for act, weight in acts:
        d[act] = d.get(act, 0) + weight
    result = [(act, weight) for act, weight in d.items()]
    result.sort(key=lambda x: -x[1])
    return result


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )
    main()
