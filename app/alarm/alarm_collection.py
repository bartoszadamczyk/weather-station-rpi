from typing import List

from .alarm import Alarm


class AlarmCollection:
    def __init__(self):
        self._collection: List[Alarm] = []

    def __iter__(self):
        yield from self._collection

    def add_alarm(self, alarm: Alarm):
        self._collection.append(alarm)
