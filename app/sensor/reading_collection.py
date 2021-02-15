from statistics import mean
from typing import List

from .reading import Reading


class ReadingCollection:
    def __init__(self, collection_size: int = 10):
        self._collection_size = collection_size
        self._collection: List[Reading] = []

    def __iter__(self):
        yield from self._collection

    def add_reading(self, reading: Reading):
        self._collection.append(reading)
        self._collection = self._collection[-self._collection_size :]

    def get_value(
        self,
        metric: str,
        window: int = 5,
    ):
        readings = [
            reading[metric]
            for reading in self._collection[-window:]
            if reading[metric] is not None
        ]
        if len(readings) > 1:
            return mean(readings)
        if len(readings) == 1:
            return readings[0]
        return None
