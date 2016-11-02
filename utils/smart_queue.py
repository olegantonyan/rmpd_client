# -*- coding: utf-8 -*-

import collections


class SmartQueue(object):
    def __init__(self, maxlen=None):
        self._deque = collections.deque(maxlen=maxlen)

    def __iter__(self):
        return self._deque.__iter__()

    def enqueue(self, obj):
        return self._deque.appendleft(obj)

    def peek(self):
        return list(self._deque)[-1]

    def dequeue(self):
        return self._deque.pop()

