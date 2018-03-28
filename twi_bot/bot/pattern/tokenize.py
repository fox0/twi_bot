# coding: utf-8
import re
from collections import OrderedDict, namedtuple
from twi_bot.bot.pattern.tokens import *

_list_tokens = (
    (TOK_ID, re.compile(r'^[\w_][\w\d_]*')),
    (TOK_COMMENT, re.compile(r'^#.*(?<!\n)')),
    (TOK_SPACE, re.compile(r'^[ \t]+')),
    (TOK_NEWLINE, re.compile(r'^\n')),

    (TOK_BEGIN_BLOCK, re.compile(r'^{')),
    (TOK_END_BLOCK, re.compile(r'^}')),

    (TOK_CONST_FLOAT, re.compile(r'^[1-9]\d*\.\d+')),
    (TOK_CONST_INT, re.compile(r'^[1-9]\d*')),

    (8, re.compile(r'^\(')),  # todo
    (9, re.compile(r'^\)')),

    (10, re.compile(r'^\.')),
    (11, re.compile(r'^,')),

    (12, re.compile(r'^-')),
    (13, re.compile(r'^\+')),
    (14, re.compile(r'^\*')),
    (15, re.compile(r'^/')),

    (16, re.compile(r'^=')),
    (17, re.compile(r'^<')),
    (18, re.compile(r'^>')),
)
tokens = OrderedDict(_list_tokens)
assert len(_list_tokens) == len(tokens)

Token = namedtuple('Token', ['tokid', 'tokval'])


class ParseError(Exception):
    pass


def tokenize(text):
    """
    Генератор. Разбивает код паттерна на токены

    :param text: код паттерна
    :return: очередной токен
    """
    numline = 1
    numcol = 0
    index = 0
    while index < len(text):
        is_found = False
        for tokid, expr in tokens.items():
            t = text[index:]
            m = expr.match(t)
            if m:
                if tokid == TOK_NEWLINE:
                    numline += 1  # todo
                is_found = True
                index += m.end()
                yield Token(tokid, m.group(0))
                break
        if not is_found:
            raise ParseError('Parse error in line %d:\n%s' % (numline, text.split('\n')[numline - 1]))
