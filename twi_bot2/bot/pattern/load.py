# coding: utf-8
import os
import logging
from twi_bot2.bot.pattern.compile import load_pattern
from twi_bot2.bot.pattern.tokenize import ParseError

log = logging.getLogger(__name__)


def load_patterns():
    result = []
    for root, dirs, files in os.walk('config/patterns'):
        # todo добавить у паттерна признак задачи
        for f in files:
            if not f.endswith('.conf'):
                continue
            filename = os.path.join(root, f)
            try:
                result.append(load_pattern(filename))
            except ParseError as e:
                log.error('filename=%s\n%s', filename, e)
    return result
