from datetime import datetime, timezone
from typing import Optional


class METRIC:
    TEMPERATURE = "HUMIDITY"
    HUMIDITY = "HUMIDITY"


class Reading:
    def __init__(
        self,
        sensor_name: str,
        sensor_model: str,
        temperature: float,
        humidity: Optional[float] = None,
    ):
        self.datetime = datetime.now(tz=timezone.utc)
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
        temperature = f"name {self.sensor_name} temperature {self.temperature:.2f}C"
        if self.humidity:
            return f"{temperature} humidity {self.humidity:.2f}"
        return temperature
