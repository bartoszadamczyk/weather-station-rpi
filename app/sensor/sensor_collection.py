import time
from typing import List, Optional

from microcontroller import Pin  # type: ignore

from .sensor import (
    discover_ds18b20_sensors,
    create_dht22_sensor,
)


class SensorCollection:
    def __init__(self, pins: Optional[List[Pin]] = None):
        self.ds18b20_sensors = discover_ds18b20_sensors()
        self.dht22_sensors = [create_dht22_sensor(pin) for pin in pins] if pins else []

    def get_all_readings(self):
        readings = []
        for sensor in self.ds18b20_sensors:
            readings.append(sensor.get_reading())
        for sensor in self.dht22_sensors:
            readings.append(sensor.get_reading())
            time.sleep(2)
        return readings
