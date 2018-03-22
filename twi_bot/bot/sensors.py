# coding: utf-8
import random


class BaseSensor(object):
    def __init__(self, name_id):
        self.id = name_id

    @property
    def value(self):
        raise NotImplementedError


class RandomSensor(BaseSensor):
    @property
    def value(self):
        return random.randrange(0, 10)
