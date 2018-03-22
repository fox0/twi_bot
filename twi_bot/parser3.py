#!/usr/bin/env python2
# coding: utf-8
from __future__ import print_function
import logging
from twi_bot.compile import load_pattern
from twi_bot.bot import Bot, PatternError
from twi_bot.sensors import RandomSensor

log = logging.getLogger(__name__)


def main():
    bot = Bot()
    bot.add_sensor(RandomSensor('coord_x'))
    bot.add_sensor(RandomSensor('coord_y'))
    bot.add_sensor(RandomSensor('wall_l'))
    bot.add_sensor(RandomSensor('wall_r'))
    bot.add_sensor(RandomSensor('wall_u'))
    bot.add_sensor(RandomSensor('wall_d'))

    patterns = [
        load_pattern('patterns/example1.conf'),
        load_pattern('patterns/example2.conf'),
    ]
    for pattern in patterns:
        try:
            pattern(bot)
        except PatternError as e:
            log.error(e)

    # noinspection PyProtectedMember
    acts = bot.act._selected_action
    # noinspection PyProtectedMember
    bot.act._reset_selected_action()
    print(acts)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG
    )
    main()
