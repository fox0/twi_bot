# coding: utf-8
from os.path import join, dirname


def get_fullpath(name, prefix='data'):
    return join(dirname(__file__), join(prefix, name))
