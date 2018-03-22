# coding: utf-8
import re

tokens = {
    'ID': re.compile(r'^[_\w][_\w\d]*'),
    'COMMENT1': re.compile(r'^#.*(?<!\n)'),
    # 'COMMENT2': re.compile(r'^//.*(?<!\n)'),
    # 'COMMENT2': re.compile(r'^\/\*.*?\*\/'),  # /* */
    'SPACE': re.compile(r'^[ \t]+'),
    'NEWLINE': re.compile(r'^\n'),
    'CONST1': re.compile(r'^[1-9]\d*'),
    'CONST2': re.compile(r'^\d+\.\d+'),

    'BEGIN_BLOCK': re.compile(r'^{'),
    'END_BLOCK': re.compile(r'^}'),
    '(': re.compile(r'^\('),
    ')': re.compile(r'^\)'),

    'DOT': re.compile(r'^\.'),
    ',': re.compile(r'^,'),

    '-': re.compile(r'^-'),
    '+': re.compile(r'^\+'),
    '*': re.compile(r'^\*'),
    '/': re.compile(r'^/'),

    '=': re.compile(r'^='),
    '<': re.compile(r'^<'),
    '>': re.compile(r'^>'),
}


class ParseError(Exception):
    pass


def tokenizer(text):
    numline = 1
    numcol = 0
    index = 0
    while index < len(text):
        is_found = False
        for pk, expr in tokens.items():
            t = text[index:]
            m = expr.match(t)
            if m:
                if pk == 'NEWLINE':
                    numline += 1  # todo
                is_found = True
                index += m.end()
                yield (pk, m.group(0))
                break
        if not is_found:
            raise ParseError('error in line %d:\n%s' % (numline, text.split('\n')[numline - 1]))
