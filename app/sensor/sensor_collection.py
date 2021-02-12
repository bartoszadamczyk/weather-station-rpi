from typing import List, Optional

from .sensor import (
    discover_ds18b20_sensors,
    create_dht22_sensor,
)


class SensorCollection:
    def __init__(self, pins: Optional[List[int]] = None):
        self.ds18b20_collection = discover_ds18b20_sensors()
        self.dht22_collection = (
            [create_dht22_sensor(pin) for pin in pins] if pins else []
        )
        self.lookup = {
            **{sensor.name: sensor for sensor in self.ds18b20_collection},
            **{sensor.name: sensor for sensor in self.dht22_collection},  # type: ignore
        }

    def keys(self):
        return list(self.lookup.keys())

    def __getitem__(self, name: str):
        return self.lookup[name]

    def __iter__(self):
        yield from self.ds18b20_collection
        yield from self.dht22_collection

    def get_all_readings(self):
        return [sensor.get_reading() for sensor in self]
