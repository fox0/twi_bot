#!/usr/bin/env python2
# coding: utf-8
import logging

from twi_bot.bot.pattern.load import load_patterns
from twi_bot.bot.pattern.interface import PatternInterfaceBot, RunTimePatternError
from twi_bot.bot.memory import Memory
from twi_bot.gui.gui import GUI

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

    step = 1  # todo

    # todo выбор задачи
    patterns = load_patterns()
    for _ in range(100):
        bot = PatternInterfaceBot(gui.get_sensors(), avalable_acts, {
            'coord_x': gui.goal.rect.centerx,
            'coord_y': gui.goal.rect.centery,
        })

        prev_node = memory.get_node(gui.bot.rect.x, gui.bot.rect.y)
        prev_node.scope = 1  # todo пока так

        # todo принимать решения на основе памяти!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        acts3 = get_command(bot, patterns)
        for command, _ in acts3:
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

            node.add_link(prev_node)

        command = acts3[0][0]
        log.info('Принято решение выполнить действие "%s"', command)

        # todo внести в класс gui?
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
        gui.update(tick=60, is_show_background=False)

    memory.show_graph()


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
    d = {}
    for act, weight in acts:
        d[act] = d.get(act, 0) + weight
    acts2 = [(act, weight) for act, weight in d.items()]
    acts2.sort(key=lambda x: -x[1])
    log.info(acts2)

    acts3 = filter(lambda x: x[1] > 0, acts2)
    log.info(acts3)
    return acts3


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )
    main()
