#!/usr/bin/env python2
# coding: utf-8
import logging.config

import numpy as np

from twi_bot.bot.pattern.load import load_patterns
from twi_bot.bot.pattern.interface import PatternInterfaceBot, RunTimePatternError
from twi_bot.bot.memory import Memory
from twi_bot.gui.gui import GUI
from twi_bot.bot.make_decision import make_desision1

log = logging.getLogger(__name__)

avalable_acts = 'go_left', 'go_right', 'go_down', 'go_up'


def main():
    step = 20
    gui = GUI(step=step, xy_bot=(110, 205), xy_goal=(280, 160), walls=(
        (80, 120),
        (100, 120),
        (120, 120),
        (140, 120),
        (160, 120),
        (180, 120),
        (180, 140),
        (180, 160),
        (180, 180),
        (180, 200),
        (180, 220),
    ))

    memory = Memory(step)

    # todo выбор задачи
    patterns = load_patterns()

    prev_command = ''

    for _ in range(200):
        bot = PatternInterfaceBot(gui.get_sensors(), avalable_acts, {
            'coord_x': gui.goal.rect.centerx,
            'coord_y': gui.goal.rect.centery,
        })

        current_node = memory.get_node(gui.bot.rect.x, gui.bot.rect.y)
        current_node.scope = 1

        acts3 = get_command(bot, patterns)

        # смотрим доступные места и запоминаем их
        for command, _ in acts3:
            node = get_node(gui, memory, command)
            current_node.add_link(node)

        # todo если мы движемся в сторону ноды, в которой не были, то до неё нужно дойти!!!

        is_found = False
        command_ = None
        for command, _ in acts3:
            node = get_node(gui, memory, command)
            if not node.scope:  # если не были в этой ноде
                command_ = command
                is_found = True
                break
        if is_found:
            log.info('Принято решение выполнить действие "%s"', command_)
            up(gui, command_)
        else:
            log.warning('oops')
            # что ж, мы зашли в тупик. Ой.
            for node in current_node.edges:
                a = 0
            pass

    memory.show_graph()


def up(gui, command):
    gui.execute_command(command)
    gui.update(tick=60,
               is_show_background=True
               )


# todo
def get_node(gui, memory, command):
    if command == 'go_right':
        node = memory.get_node(gui.bot.rect.x + gui.step, gui.bot.rect.y)
    elif command == 'go_left':
        node = memory.get_node(gui.bot.rect.x - gui.step, gui.bot.rect.y)
    elif command == 'go_down':
        node = memory.get_node(gui.bot.rect.x, gui.bot.rect.y + gui.step)
    elif command == 'go_up':
        node = memory.get_node(gui.bot.rect.x, gui.bot.rect.y - gui.step)
    else:
        raise NotImplementedError
    return node


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


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )
    # logging.config.fileConfig('config/logging.conf')
    main()
