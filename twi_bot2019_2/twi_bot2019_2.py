# coding: utf-8
import logging

__version__ = '0.4.0'

log = logging.getLogger(__name__)


def main():
    pass


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
        level=logging.DEBUG
    )
    main()
