# coding: utf-8
import re
from twi_bot.parse.tokens import *

tokens_list = {
    TOK_ID: re.compile(r'^[_\w][_\w\d]*'),
    TOK_COMMENT1: re.compile(r'^#.*(?<!\n)'),
    # 'COMMENT2': re.compile(r'^//.*(?<!\n)'),
    # 'COMMENT2': re.compile(r'^\/\*.*?\*\/'),  # /* */
    TOK_SPACE: re.compile(r'^[ \t]+'),
    TOK_NEWLINE: re.compile(r'^\n'),

    TOK_BEGIN_BLOCK: re.compile(r'^{'),
    TOK_END_BLOCK: re.compile(r'^}'),
    6: re.compile(r'^\('),  # todo
    7: re.compile(r'^\)'),

    8: re.compile(r'^[1-9]\d*'),
    9: re.compile(r'^\d+\.\d+'),

    10: re.compile(r'^\.'),
    11: re.compile(r'^,'),

    12: re.compile(r'^-'),
    13: re.compile(r'^\+'),
    14: re.compile(r'^\*'),
    15: re.compile(r'^/'),

    16: re.compile(r'^='),
    17: re.compile(r'^<'),
    18: re.compile(r'^>'),
}


class ParseError(Exception):
    pass


def tokenize(text):
    """
    Генератор. Разбивает код паттерна на токены

    :param text: код паттерна
    :return: очередной токен (tokid, tokval)
    """
    numline = 1
    numcol = 0
    index = 0
    while index < len(text):
        is_found = False
        for tokid, expr in tokens_list.items():
            t = text[index:]
            m = expr.match(t)
            if m:
                if tokid == TOK_NEWLINE:
                    numline += 1  # todo
                is_found = True
                index += m.end()
                yield (tokid, m.group(0))
                break
        if not is_found:
            raise ParseError('Parse error in line %d:\n%s' % (numline, text.split('\n')[numline - 1]))
