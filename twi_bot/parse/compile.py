#!/usr/bin/env python2
# coding: utf-8
import os
import marshal
import logging

from twi_bot.parse.tokenize import tokenize
from twi_bot.parse.tokens import *

log = logging.getLogger(__name__)
FUNC_NAME = '__pattern'


def load_pattern(filename_pattern, use_cache=True):
    """
    Загрузить паттерн из файла

    :param filename_pattern: имя файла-паттерна
    :param use_cache: флаг использования кеша байт-кода
    :return: скомпилированная функция паттерна
    """
    filename_bytecode = '%s_%s.pyc' % (os.path.abspath(filename_pattern), os.path.getmtime(filename_pattern))
    if use_cache and os.path.exists(filename_bytecode):
        log.debug('load bytecodes from %s', filename_bytecode)
        with open(filename_bytecode, 'rb') as f:
            code = marshal.load(f)
    else:
        log.debug('load pattern from %s', filename_pattern)
        with open(filename_pattern) as f:
            text = f.read()
        py = pattern2python(text)
        log.debug('\n%s', py)
        code = compile(py, '<%s>' % filename_pattern, 'exec')
        if use_cache:
            with open(filename_bytecode, 'wb') as f:
                marshal.dump(code, f)

    ns = {}
    exec code in ns
    return ns[FUNC_NAME]


def pattern2python(text):
    """
    Переводит код паттерна в язык программирования python

    :param text: код паттерна
    :return: код на питоне
    """
    # удаляем начальные и конечные пробелы в строках
    text = '\n'.join(line.strip() for line in text.split('\n'))
    s = tokenize(text)
    result = [
        '# coding: utf-8',
        '\n',
        '# DO NOT EDIT THIS!',
        '\n',
        'def %s(bot):' % FUNC_NAME,
        '\n',
    ]
    tabs = 4
    try:
        while True:
            tokid, tokval = next(s)
            if tokid == TOK_COMMENT1:
                continue
            if tokid == TOK_NEWLINE:
                result.append('\n')
                result.append(' ' * tabs)
                continue
            if tokid == TOK_BEGIN_BLOCK:
                tabs += 4
                if result[-1] == ' ':
                    result.pop()
                result.append(':')
                result.append('\n')
                result.append(' ' * tabs)
                result.append('pass')
                result.append('\n')
                result.append(' ' * tabs)
                continue
            if tokid == TOK_END_BLOCK:
                tabs -= 4
                result.append('\n')
                result.append(' ' * tabs)
                continue
            if tokid == TOK_SPACE:
                if result[-1][-1] != ' ':
                    result.append(' ')
                continue
            if tokid == TOK_ID:
                val = {
                    'function': 'def',
                    'elseif': 'elif',
                }.get(tokval, tokval)
                result.append(val)
                continue
            result.append(tokval)
    except StopIteration:
        r = ''.join(result)
        # удалить пустые строки
        r2 = '\n'.join(line for line in r.split('\n') if line.strip())
        return r2
