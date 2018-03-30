# coding: utf-8
import logging

from twi_bot.bot.pattern.interface import PatternInterfaceBot, RunTimePatternError, Intent

log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)


def execute_patterns(bot, patterns):
    """
    Запускает паттерны.

    Возвращает список намерений, отсортированный по убыванию
    """
    assert isinstance(bot, PatternInterfaceBot)
    for pattern in patterns:
        try:
            pattern(bot)
        except RunTimePatternError as e:
            log.error(e)
        except BaseException as e:
            log.exception(e)

    # noinspection PyProtectedMember
    acts = bot.act._selected
    log.debug('acts=%s', acts)

    # суммируем намерения от всех паттернов
    d = {}
    for act, weight in acts:
        d[act] = d.get(act, 0) + weight

    result = [Intent(act, weight) for act, weight in d.items() if weight > 0]
    result.sort(key=lambda x: -x.weight)
    log.info(result)
    return result
