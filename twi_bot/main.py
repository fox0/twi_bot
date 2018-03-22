#!/usr/bin/env python2
# coding: utf-8
from __future__ import print_function  # , unicode_literals
import logging

from twi_bot.parse.compile import load_pattern
from twi_bot.parse.tokenizer import ParseError
from twi_bot.bot.bot import Bot
from twi_bot.bot.sensors import RandomSensor
from twi_bot.bot.acts import BaseAct
from twi_bot.bot.task import RandomTaskParam

log = logging.getLogger(__name__)


def main():
    bot = get_bot()
    patterns = get_patterns()

    # todo выбор задачи

    task_params = [
        RandomTaskParam('coord_x'),
        RandomTaskParam('coord_y'),
    ]

    # todo фильтрация паттернов перед запуском
    act = make_desision1(bot, patterns, task_params)


def make_desision1(bot, patterns, task_params=None):
    acts = bot.make_desision(patterns, task_params)
    log.debug('acts=%s', acts)
    acts2 = sum_result(acts)
    log.info(acts2)
    acts3 = filter(lambda x: x[1] > 0, acts2)
    log.info(acts3)

    # todo
    act = None
    try:
        act = acts3[0]
    except IndexError:
        try:
            act = acts2[0]
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


def get_bot():
    bot = Bot()

    bot.add_sensor(RandomSensor('coord_x'))
    bot.add_sensor(RandomSensor('coord_y'))
    bot.add_sensor(RandomSensor('wall_l'))
    bot.add_sensor(RandomSensor('wall_r'))
    bot.add_sensor(RandomSensor('wall_u'))
    bot.add_sensor(RandomSensor('wall_d'))

    bot.add_act(BaseAct('go_left'))
    bot.add_act(BaseAct('go_up'))
    bot.add_act(BaseAct('go_right'))
    bot.add_act(BaseAct('go_down'))

    return bot


def get_patterns():
    # todo добавить у паттерна признак задачи
    result = []
    ls = ['patterns/example1.conf', 'patterns/example2.conf']
    for filename in ls:
        try:
            result.append(load_pattern(filename))
        except ParseError as e:
            log.error('filename=%s\n%s', filename, e)
    return result


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )
    main()
