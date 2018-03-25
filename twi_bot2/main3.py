#!/usr/bin/env python2
# coding: utf-8
import logging
import traceback

# import networkx as nx

from twi_bot2.bot.pattern.load import load_patterns
from twi_bot2.bot.pattern.interface import PatternInterfaceBot, RunTimePatternError
from twi_bot2.gui.gui import GUI

log = logging.getLogger(__name__)

avalable_acts = ['go_left', 'go_right', 'go_down', 'go_up']


def main():
    gui = GUI()
    step = 10

    # todo выбор задачи
    patterns = load_patterns()
    while True:
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

        command = get_command(bot, patterns)

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
    # todo
    act = None
    try:
        act = acts3[0][0]
    except IndexError:
        try:
            act = acts2[0][0]
        except IndexError:
            pass
    log.info('Принято решение выполнить действие "%s"', act)
    return act


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
