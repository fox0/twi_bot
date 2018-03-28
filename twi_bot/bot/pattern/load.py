# coding: utf-8
import os
import logging
from twi_bot.bot.pattern.compile import load_pattern
from twi_bot.bot.pattern.tokenize import ParseError

log = logging.getLogger(__name__)


def load_patterns():
    result = []
    for root, dirs, files in os.walk('config/patterns'):
        # todo добавить у паттерна признак задачи
        for f in files:
            if not f.endswith('.pattern'):
                continue
            filename = os.path.join(root, f)
            try:
                pattern = load_pattern(filename)
                result.append(pattern)
            except ParseError as e:
                log.error('filename=%s\n%s', filename, e)
            except BaseException as e:
                log.exception(e)
    return result
