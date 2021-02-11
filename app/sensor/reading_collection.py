from statistics import mean
from typing import List

from .reading import Reading


class ReadingCollection:
    def __init__(self, collection_size: int = 5):
        self.collection_size = collection_size
        self.collection: List[Reading] = []

    def add_reading(self, reading: Reading):
        self.collection.append(reading)
        self._trim_collection()

    def _trim_collection(self):
        self.collection = self.collection[-self.collection_size :]

    def get_average_temperature(self):
        temperature_readings = [
            reading.temperature
            for reading in self.collection
            if reading.temperature is not None
        ]
        return mean(temperature_readings) if len(temperature_readings) else None

    def get_average_humidity(self):
        humidity_readings = [
            reading.humidity
            for reading in self.collection
            if reading.humidity is not None
        ]
        return mean(humidity_readings) if len(humidity_readings) else None

    def get_latest_reading(self):
        return self.collection[-1]
