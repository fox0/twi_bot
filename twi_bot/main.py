#!/usr/bin/env python2
# coding: utf-8
import logging

from twi_bot.bot.pattern.load import load_patterns
from twi_bot.bot.pattern.interface import PatternInterfaceBot
from twi_bot.bot.memory import Memory
from twi_bot.gui.gui import GUI
from twi_bot.bot.make_decision import execute_patterns

log = logging.getLogger('twi_bot.main')

avalable_acts = 'go_left', 'go_right', 'go_down', 'go_up'


def main():
    step = 20
    gui = GUI(
        step=step, xy_bot=(91, 212), xy_goal=(280, 160), walls=(
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
        ),
        tick=60,
        # is_show_background=True
    )

    patterns = load_patterns()

    # todo выбор задачи

    memory = Memory(step)

    prev_command = ''
    prev_node = None

    for _ in range(780):
        bot = PatternInterfaceBot(gui.get_sensors(), avalable_acts, {
            'coord_x': gui.goal.rect.centerx,
            'coord_y': gui.goal.rect.centery,
        })
        intents = execute_patterns(bot, patterns)
        acts = [i.act for i in intents]

        current_node = memory.get_node(gui.bot.rect.x, gui.bot.rect.y)
        current_node.scope = bot.math.sqrt((bot.task.coord_x - gui.bot.rect.x) ** 2 +
                                           (bot.task.coord_y - gui.bot.rect.y) ** 2)  # todo

        if prev_node == current_node and prev_command in acts:
            # мы уже приняли решение и продолжаем его выполнять
            gui.update(prev_command)
            continue

        # смотрим доступные места и запоминаем их
        for command in acts:
            node = get_node(gui, memory, command)  # todo добавляет лишние 2-3!
            current_node.add_link(node)

        command = get_command(gui, memory, acts)
        if command:
            log.info('%s Принято решение выполнить действие "%s"', current_node, command)
            gui.update(command)
            prev_node = current_node
            prev_command = command
            continue

        log.warning('oops')
        # что ж, мы зашли в тупик. Ой.
        for node in current_node.edges:
            a = 0
        pass

    memory.show_graph()


def get_command(gui, memory, acts):
    for command in acts:
        node = get_node(gui, memory, command)
        if not node.scope:  # если не были в этой ноде
            return command
    return None


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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
