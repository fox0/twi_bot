# coding: utf-8
import random


class TaskParam(object):
    def __init__(self, name_id):
        self.id = name_id

    # @property
    # def value(self):
    #     raise NotImplementedError


class RandomTaskParam(TaskParam):
    @property
    def value(self):
        return random.randrange(0, 10)
