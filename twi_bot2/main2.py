#!/usr/bin/env python2
# coding: utf-8
import os
import logging
from twi_bot2.pattern.parser import pattern2python

log = logging.getLogger('twi_bot.main')


def main():
    filename = 'conf/example1.pattern'
    funcname = 'example1'
    with open(filename) as f:
        args, text = pattern2python(f.read(), funcname)
    log.debug('\n%s', text)

    # todo 'example1' - имя конфига
    filename2 = '%s_%d' % ('example1', os.path.getmtime(filename))
    # todo join
    with open('%s/%s.py' % (os.path.abspath('cache'), filename2), 'w') as f:
        f.write(text)

    ls = ['twi_bot2', 'cache', filename2]
    func = __import__('.'.join(ls))
    for i in ls[1:] + [funcname]:
        func = func.__getattribute__(i)

    for i in func(42, 41):
        print(i)
    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
