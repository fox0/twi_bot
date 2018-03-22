#!/usr/bin/env python2
# coding: utf-8
import logging
from twi_bot.tokenizer import tokenizer

log = logging.getLogger(__name__)
FUNC_NAME = '__pattern'


def load_pattern(filename):
    """
    Подгрузить паттерн из файла

    :param filename: имя файла-паттерна
    :return: скомпилированная функция паттерна
    """
    with open(filename) as f:
        text = f.read()

    py = _pattern2python(text)
    log.debug(py)

    code = compile(py, '<%s>' % filename, 'exec')
    ns = {}
    exec code in ns
    return ns[FUNC_NAME]


def _pattern2python(text):
    s = tokenizer(text)
    result = [
        '# coding: utf-8',
        '\n',
        'def %s(bot):' % FUNC_NAME,
        '\n',
    ]
    tabs = 4
    is_begin = True
    try:
        while True:
            tokid, tokval = next(s)
            if tokid == 'COMMENT1':
                continue
            if tokid == 'NEWLINE':
                result.append('\n')
                is_begin = True
                continue
            if tokid == 'BEGIN_BLOCK':
                tabs += 4
                result.append(':')
                result.append('\n')
                is_begin = True
                continue
            if tokid == 'END_BLOCK':
                tabs -= 4
                result.append('\n')
                is_begin = True
                continue
            if tokid == 'ID' and tokval == 'function':
                tokval = 'def'

            if is_begin and tokid != 'SPACE':
                el = '%s%s' % (' ' * tabs, tokval)  # todo ставит на 4 пробела больше, чем надо
                is_begin = False
            else:
                el = tokval
            result.append(el)
    except StopIteration:
        r = ''.join(result)
        r2 = [line for line in r.split('\n') if line.strip()]
        return '\n'.join(r2)
