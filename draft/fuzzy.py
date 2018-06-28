#!/usr/bin/env python2
# coding: utf-8


class Fuzzy(object):
    """Максиминный подход"""

    def __init__(self, value):
        assert 0. < value < 1.
        self.value = value

    def __or__(self, other):
        return max(self.value, other.value)

    def __and__(self, other):
        return min(self.value, other.value)

    def not_(self):
        return 1 - self.value


class Fuzzy2(object):
    """Колорометрический подход"""

    def __init__(self, value):
        assert 0. < value < 1.
        self.value = value

    def __or__(self, other):
        assert isinstance(other, Fuzzy2)
        return self.value + other.value - self.value * other.value

    def __and__(self, other):
        assert isinstance(other, Fuzzy2)
        return self.value * other.value

    def not_(self):
        return 1 - self.value


if __name__ == '__main__':
    cls = Fuzzy2
    a, b = cls(0.3), cls(0.8)
    print((a or b).value)
    print((a and b).value)
    print(a.not_())
