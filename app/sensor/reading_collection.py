from statistics import mean
from typing import List

from .reading import Reading


class ReadingCollection:
    def __init__(self, collection_size: int = 5):
        self.collection_size = collection_size
        self.collection: List[Reading] = []

    def __iter__(self):
        yield from self.collection

    def add_reading(self, reading: Reading):
        self.collection.append(reading)
        self.collection = self.collection[-self.collection_size :]

    def get_average_temperature(self):
        temperature_readings = [
            reading.temperature for reading in self if reading.temperature is not None
        ]
        return mean(temperature_readings) if len(temperature_readings) else None

    def get_average_humidity(self):
        humidity_readings = [
            reading.humidity for reading in self if reading.humidity is not None
        ]
        return mean(humidity_readings) if len(humidity_readings) else None
