#!/usr/bin/env python2
# coding: utf-8
import logging
import traceback

from twi_bot2.bot.pattern.load import load_patterns
from twi_bot2.bot.pattern.interface import PatternInterfaceBot, RunTimePatternError

log = logging.getLogger(__name__)


def main():
    patterns = load_patterns()

    # todo выбор задачи

    bot = PatternInterfaceBot(
        sensors={
            'wall_l': 10,
            'wall_r': 10,
            'wall_u': 10,
            'wall_d': 10,
            'coord_x': 5,
            'coord_y': 5,
        },
        acts=[
            'go_left',
            'go_right',
            'go_down',
            'go_up',
        ],
        task_params={
            'coord_x': 100,
            'coord_y': 100,
        }
    )

    for pattern in patterns:
        try:
            pattern(bot)
        except RunTimePatternError as e:
            log.error(e)
        except BaseException:
            log.fatal(traceback.format_exc())
    # noinspection PyProtectedMember
    acts = bot.act._selected
    print(acts)


#
# def make_desision1(bot, patterns, task_params=None):
#     acts = bot.make_desision(patterns, task_params)
#     log.debug('acts=%s', acts)
#     acts2 = sum_result(acts)
#     log.info(acts2)
#     acts3 = filter(lambda x: x[1] > 0, acts2)
#     log.info(acts3)
#
#     # todo
#     act = None
#     try:
#         act = acts3[0]
#     except IndexError:
#         try:
#             act = acts2[0]
#         except IndexError:
#             pass
#     log.info('Принято решение выполнить действие "%s"', act)
#     return act
#
#
# def sum_result(acts):
#     d = {}
#     for act, weight in acts:
#         d[act] = d.get(act, 0) + weight
#     result = [(act, weight) for act, weight in d.items()]
#     result.sort(key=lambda x: -x[1])
#     return result


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )
    main()
