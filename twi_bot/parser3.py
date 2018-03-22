#!/usr/bin/env python2
# coding: utf-8
import re
from twi_bot.parser2 import tokenizer, ParseError


def main():
    filename = 'patterns/example1.conf'
    with open(filename) as f:
        text = f.read()

    s = tokenizer(text)
    result = [
        '# coding: utf-8',
        '\n',
        '# NOT EDIT! Generated ?',
        '\n',
        'def __pattern(bot):',
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

            if tokid == 'ID':
                # if tokval == 'bot':
                #     tokid, tokval = next(s)
                #     if tokid != 'DOT':
                #         raise ParseError('Ожидалась точка')
                #     raise NotImplementedError(tokval)
                if tokval == 'function':
                    raise NotImplementedError(tokval)

            if is_begin and tokid != 'SPACE':
                el = '%s%s' % (' ' * tabs, tokval)
                is_begin = False
            else:
                el = tokval
            result.append(el)
    except StopIteration:
        r = ''.join(result)
        r2 = [line for line in r.split('\n') if line.strip()]
        py = '\n'.join(r2)
        # print(py)

        code = compile(py, '<%s>' % filename, 'exec')
        ns = {}
        exec code in ns
        __pattern = ns['__pattern']

        class Sensors(object):
            def __getattr__(self, item):
                if item not in ['wall_l', 'wall_r', 'wall_u', 'wall_d']:
                    raise ParseError('Датчика "%s" не существует' % item)
                if item == 'wall_r':
                    return 4
                return 10

        class Act(object):
            def __getattr__(self, item):
                if item not in ['go_left', 'go_right', 'go_up', 'go_down']:
                    raise ParseError('Действия "%s" не существует' % item)

                def func(weight):
                    print(item, weight)

                return func

        class Bot(object):
            def __init__(self):
                self.sensors = Sensors()
                self.act = Act()

        bot = Bot()
        __pattern(bot)


if __name__ == '__main__':
    main()
