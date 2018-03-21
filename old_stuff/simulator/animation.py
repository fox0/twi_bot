# coding: utf-8
import time
from itertools import cycle


class Animation(object):
    def __init__(self, surface, frames, delay=0.1):
        self.surface = surface
        self.frame_generator = cycle(frames)
        self._next_frame()
        self.delay = delay
        self.start_time = time.time()

    def update(self):
        current_time = time.time()
        if current_time - self.start_time > self.delay:
            self.start_time = current_time
            self._next_frame()
        self.surface.blit(self.frame, (0, 0))

    def _next_frame(self):
        self.frame = self.frame_generator.next()  # py2
