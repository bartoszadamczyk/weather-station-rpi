from datetime import datetime, timezone
from statistics import mean
from typing import Optional, List


class METRIC:
    TEMPERATURE = "HUMIDITY"
    HUMIDITY = "HUMIDITY"


class Reading:
    def __init__(
        self,
        device_uuid: str,
        sensor_name: str,
        sensor_model: str,
        temperature: float,
        humidity: Optional[float] = None,
    ):
        self.datetime = datetime.now(tz=timezone.utc)
        self.device_uuid = device_uuid
        self.sensor_name = sensor_name
        self.sensor_model = sensor_model
        self.temperature = temperature
        self.humidity = humidity

    def get(self):
        return [METRIC.TEMPERATURE, METRIC.HUMIDITY]

    def __getitem__(self, metric: str):
        if metric == METRIC.TEMPERATURE:
            return self.temperature
        if metric == METRIC.HUMIDITY:
            return self.humidity
        return None

    def __str__(self):
        temperature = f"{self.sensor_name} temperature {self.temperature:.2f}C"
        if self.humidity:
            return f"{temperature} humidity {self.humidity:.2f}"
        return temperature


class ReadingCollection:
    def __init__(self, max_size: int = 10):
        self._max_size = max_size
        self._collection: List[Reading] = []

    def __iter__(self):
        yield from self._collection

    def add_reading(self, reading: Reading):
        self._collection.insert(0, reading)
        self._collection = self._collection[0 : self._max_size]

    def get_value(self, metric: str = METRIC.TEMPERATURE, window: int = 5):
        readings = [
            reading[metric]
            for reading in self._collection[0:window]
            if reading[metric] is not None
        ]
        if len(readings) > 1:
            return mean(readings)
        if len(readings) == 1:
            return readings[0]
        return None
