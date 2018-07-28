# coding: utf-8
import logging
from twi_bot2.pattern.load import get_patterns

log = logging.getLogger('twi_bot.main')


def main():
    patterns = get_patterns()
    print(patterns)
    for i in patterns[0][1](42, 41):
        print(i)
    pass


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
        level=logging.DEBUG
    )
    main()
