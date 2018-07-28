# coding: utf-8
from twi_bot2.kernel.pattern.tokenize import tokenize, ParseError
from twi_bot2.kernel.pattern.tokens import *


def pattern2python(text, func_name='func'):
    result = ['''\
# coding: utf-8
# DO NOT EDIT THIS!
# __builtins__ = {}
''']
    args = []

    g = tokenize(text)
    # dev
    while True:
        tokid, tokval = next(g)
        if tokid in (TOK_COMMENT, TOK_NEWLINE, TOK_SPACE):
            continue
        if tokid != TOK_ID or tokval != 'dev':
            raise ParseError(u"ожидалось 'dev', найдено '%s'" % tokval)
        break
    # {
    while True:
        tokid, tokval = next(g)
        if tokid in (TOK_COMMENT, TOK_NEWLINE, TOK_SPACE):
            continue
        if tokid != TOK_BEGIN_BLOCK:
            raise ParseError(u"ожидалось '{', найдено '%s'" % tokval)
        break
    # …}
    while True:
        tokid, tokval = next(g)
        if tokid in (TOK_COMMENT, TOK_NEWLINE, TOK_SPACE):
            continue
        if tokid == TOK_ID:
            args.append(tokval)
            continue
        if tokid == TOK_END_BLOCK:
                break
        raise ParseError(u"ожидалось 'id' или '}', найдено '%s'" % tokval)
    result.append('def %s(%s):' % (func_name, ', '.join(args)))

    while True:
        tokid, tokval = next(g)
        if tokid in (TOK_COMMENT, TOK_NEWLINE, TOK_SPACE):
            continue
        if tokid != TOK_ID or tokval != 'code':
            raise ParseError(u"ожидалось 'code', найдено '%s'" % tokval)
        break
    while True:
        tokid, tokval = next(g)
        if tokid in (TOK_COMMENT, TOK_NEWLINE, TOK_SPACE):
            continue
        if tokid != TOK_BEGIN_BLOCK:
            raise ParseError(u"ожидалось '{', найдено '%s'" % tokval)
        break

    tabs = 4
    try:
        while True:
            tokid, tokval = next(g)
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
                    'act': 'yield',
                }.get(tokval, tokval)
                result.append(val)
                continue
            result.append(tokval)
    except StopIteration:
        r = ''.join(result)
        # удалить пустые строки
        # r = '\n'.join(line for line in r.split('\n') if line.strip())
        # r = r.replace('def', '\n\ndef')
        r = '%s\n' % r
        return tuple(args), r
