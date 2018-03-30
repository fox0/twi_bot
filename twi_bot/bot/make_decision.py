# coding: utf-8
import logging

from twi_bot.bot.pattern.interface import PatternInterfaceBot, RunTimePatternError

log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)


def execute_patterns(bot, patterns):
    assert isinstance(bot, PatternInterfaceBot)
    for pattern in patterns:
        try:
            pattern(bot)
        except RunTimePatternError as e:
            log.error(e)
        except BaseException as e:
            log.exception(e)
    return make_desision1(bot)


def make_desision1(bot):
    # noinspection PyProtectedMember
    acts = bot.act._selected
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
