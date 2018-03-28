#!/usr/bin/env python2
# coding: utf-8
import logging

import matplotlib.pyplot as plt
import networkx as nx

from twi_bot.bot.pattern.load import load_patterns
from twi_bot.bot.pattern.interface import PatternInterfaceBot, RunTimePatternError
from twi_bot.bot.memory import Memory
from twi_bot.gui.gui import GUI

log = logging.getLogger(__name__)

avalable_acts = 'go_left', 'go_right', 'go_down', 'go_up'


def main():
    graph = nx.Graph()

    gui = GUI(step=20, xy_bot=(20, 160), xy_goal=(280, 160), walls=(
        (180, 120),
        (180, 140),
        (180, 160),
        (180, 180),
        (180, 200),
    ))

    memory = Memory()

    step = 1  # todo

    # todo выбор задачи
    patterns = load_patterns()
    for _ in range(20):
        bot = PatternInterfaceBot(get_sensors(gui), avalable_acts, {
            'coord_x': gui.goal.rect.x,
            'coord_y': gui.goal.rect.y,
        })

        prev_node = memory.get_node(gui.bot.rect.x, gui.bot.rect.y)

        acts3 = get_command(bot, patterns)
        for command, _ in acts3:
            if command == 'go_right':
                node = memory.get_node(gui.bot.rect.x + step, gui.bot.rect.y)
            elif command == 'go_left':
                node = memory.get_node(gui.bot.rect.x - step, gui.bot.rect.y)
            elif command == 'go_down':
                node = memory.get_node(gui.bot.rect.x, gui.bot.rect.y + step)
            elif command == 'go_up':
                node = memory.get_node(gui.bot.rect.x, gui.bot.rect.y - step)
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


def get_sensors(gui):
    sensors = {
        'wall_l': 10,
        'wall_r': 10,
        'wall_u': 10,
        'wall_d': 10,
        'coord_x': gui.bot.rect.x,
        'coord_y': gui.bot.rect.y,
    }
    for wall in gui.walls:
        if wall.rect.collidepoint(gui.bot.rect.x + gui.step, gui.bot.rect.y):
            sensors['wall_r'] = 0
        if wall.rect.collidepoint(gui.bot.rect.x - gui.step, gui.bot.rect.y):
            sensors['wall_l'] = 0
        if wall.rect.collidepoint(gui.bot.rect.x, gui.bot.rect.y + gui.step):
            sensors['wall_d'] = 0
        if wall.rect.collidepoint(gui.bot.rect.x, gui.bot.rect.y - gui.step):
            sensors['wall_u'] = 0
    return sensors


def get_command(bot, patterns):
    for pattern in patterns:
        try:
            pattern(bot)
        except RunTimePatternError as e:
            log.error(e)
        except BaseException as e:
            log.exception(e)
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
