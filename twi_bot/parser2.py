# coding: utf-8
import re
from collections import namedtuple

# T_ID = 0
#
# Token = namedtuple('Token', ['tok', 'value'])

tokens = {
    'ID': re.compile(r'^[_\w][_\w\d]*'),
    'COMMENT1': re.compile(r'^#.*(?<!\n)'),
    # 'COMMENT2': re.compile(r'^//.*(?<!\n)'),
    # 'COMMENT2': re.compile(r'^\/\*.*?\*\/'),  # /* */
    'SPACE': re.compile(r'^ +'),
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
        # if text[index] in (' ', '\t'):
        #     index += 1
        #     continue

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


def main():
    with open('patterns/example1.conf') as f:
        text = f.read()

    def e_s():
        tokid, tokval = next(s)
        if tokid in ('COMMENT1', 'NEWLINE'):
            return
        elif tokid == 'ID':
            if tokval == 'function':
                raise NotImplementedError
            elif tokval == 'bot':
                e_act()
            else:
                e_id(tokval)
        else:
            raise NotImplementedError(tokid)

    def e_id(name_id):
        tokid, tokval = next(s)
        if tokid == '=':
            raise NotImplementedError(tokid)
        raise NotImplementedError(tokid)

    def e_act():
        tokid, tokval = next(s)
        if tokid != 'ID' or tokval != 'bot':
            raise ParseError('Ожидалось %s, найдено: %s' % ('bot', tokval))
        raise NotImplementedError(tokid)

    s = tokenizer(text)
    result = []
    tabs = 0
    try:
        while True:
            e_s()
    except StopIteration:
        print(result)


if __name__ == '__main__':
    main()
