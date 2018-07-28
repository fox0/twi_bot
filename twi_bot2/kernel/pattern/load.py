# coding: utf-8
import os
import logging
from twi_bot2.kernel.pattern.parser import pattern2python

log = logging.getLogger(__name__)


def get_patterns(config_dir='conf', cache_dir='cache'):
    result = []
    for filename in _get_configs(config_dir):
        config, _ = os.path.splitext(os.path.basename(filename))
        cache_key = '%s_%d' % (config, os.path.getmtime(filename))
        filename_py = '%s.py' % os.path.join(cache_dir, cache_key)
        # if os.path.exists(filename_py):
        #     log.debug('load from cache %s', filename_py)
        #     todo ags
        # else:
        log.debug('parsing %s', filename)
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


def _get_configs(config_dir):
    result = []
    for i in os.listdir(config_dir):
        if not i.endswith('.conf'):
            continue
        f = os.path.join(config_dir, i)
        # if os.path.isfile(f):
        result.append(f)
    return result
