#!/usr/bin/env python2
# coding: utf-8
from __future__ import print_function
import logging
from twi_bot.compile import load_pattern
from twi_bot.bot import Bot
from twi_bot.sensors import RandomSensor

log = logging.getLogger(__name__)


def main():
    bot = get_bot()
    patterns = get_patterns()

    # todo фильтрация паттернов перед запуском
    acts = bot.make_desision(patterns)
    print(acts)


def get_bot():
    bot = Bot()
    bot.add_sensor(RandomSensor('coord_x'))
    bot.add_sensor(RandomSensor('coord_y'))
    bot.add_sensor(RandomSensor('wall_l'))
    bot.add_sensor(RandomSensor('wall_r'))
    bot.add_sensor(RandomSensor('wall_u'))
    bot.add_sensor(RandomSensor('wall_d'))
    return bot


def get_patterns():
    # todo добавить у паттерна признак задачи
    patterns = [
        load_pattern('patterns/example1.conf'),
        load_pattern('patterns/example2.conf'),
    ]
    return patterns


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )
    main()
