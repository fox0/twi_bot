# coding: utf-8
import os
import logging
from twi_bot2.pattern.parser import pattern2python

log = logging.getLogger('twi_bot.main')
PREFIX_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    patterns = _get_patterns()
    print(patterns)
    pass


def _get_patterns():
    """

    :return: спискок паттернов: (аргументы, функция)
    """
    result = []
    for filename in _get_configs():
        log.debug('%s', filename)
        config, _ = os.path.splitext(os.path.basename(filename))
        cache_key = '%s_%d' % (config, os.path.getmtime(filename))
        filename_py = '%s.py' % os.path.join(os.path.join(PREFIX_DIR, 'cache'), cache_key)
        # if not os.path.exists(filename_py):
        with open(filename, 'r') as f:
            args, text = pattern2python(f.read(), config)
        log.debug('\n%s', text)
        with open(filename_py, 'w') as f:
            f.write(text)

        module = '.'.join(('twi_bot2', 'cache', cache_key))
        func = __import__(module)
        for i in 'cache', cache_key, config:
            func = func.__getattribute__(i)
        result.append((args, func))
    return result


def _get_configs():
    """

    :return: список конфигов
    """
    result = []
    d = os.path.join(PREFIX_DIR, 'conf')
    for i in os.listdir(d):
        if not i.endswith('.conf'):
            log.debug('ignore file %s', i)
            continue
        f = os.path.join(d, i)
        # if os.path.isfile(f):
        result.append(f)
    return result


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
