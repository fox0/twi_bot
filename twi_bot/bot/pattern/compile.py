#!/usr/bin/env python2
# coding: utf-8
import os
import marshal
import logging

from twi_bot.bot.pattern.tokenize import tokenize
from twi_bot.bot.pattern.tokens import *

log = logging.getLogger(__name__)


def load_pattern(filename_pattern, use_cache=True):
    """
    Загрузить паттерн из файла

    :param filename_pattern: имя файла-паттерна
    :param use_cache: флаг использования кеша байт-кода
    :return: скомпилированная функция паттерна
    """
    filename_bytecode = _get_filename_bytecode(filename_pattern)
    func_name = _get_func_name(filename_pattern)
    if use_cache and os.path.exists(filename_bytecode):
        log.debug('load bytecodes from %s', filename_bytecode)
        with open(filename_bytecode, 'rb') as f:
            code = marshal.load(f)
    else:
        log.debug('load pattern from %s', filename_pattern)
        with open(filename_pattern) as f:
            text = f.read()

        py = pattern2python(text, func_name)

        log.debug('\n%s', py)
        code = compile(py, '<%s>' % os.path.abspath(filename_pattern), 'exec')
        if use_cache:
            with open(filename_bytecode, 'wb') as f:
                marshal.dump(code, f)

    ns = {}
    exec code in ns
    return ns[func_name]


def _get_filename_bytecode(filename_pattern):
    return '%s_%s.pyc' % (os.path.abspath(filename_pattern), os.path.getmtime(filename_pattern))


def _get_func_name(filename_pattern):
    return 'pattern_' + os.path.basename(filename_pattern).rsplit('.', 1)[0].replace('.', '_')


python_template = '''\
# coding: utf-8
# DO NOT EDIT THIS!
__builtins__ = {}

def %s(bot):
'''


def pattern2python(text, func_name):
    """
    Переводит код паттерна в язык программирования python

    :param text: код паттерна
    :param func_name:
    :return: код на питоне
    """
    s = tokenize(text)
    result = [python_template % func_name]
    tabs = 4
    try:
        while True:
            tokid, tokval = next(s)
            if tokid == TOK_COMMENT:
                continue
            if tokid == TOK_NEWLINE:
                result.extend(('\n', ' ' * tabs))
                continue
            if tokid == TOK_BEGIN_BLOCK:
                tabs += 4
                if result[-1] == ' ':
                    result.pop()
                result.extend((':\n', ' ' * tabs, 'pass\n', ' ' * tabs))
                continue
            if tokid == TOK_END_BLOCK:
                tabs -= 4
                result.extend(('\n', ' ' * tabs))
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
