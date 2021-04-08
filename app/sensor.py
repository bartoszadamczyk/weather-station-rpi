from abc import ABC, abstractmethod
from typing import Optional, List

import asyncio
from adafruit_dht import DHT22  # type: ignore
from adafruit_blinka.microcontroller.bcm283x.pin import Pin  # type: ignore
from w1thermsensor import W1ThermSensor  # type: ignore

from .async_handler import run_in_executor
from .constants import MODEL, METRIC
from .helper import get_cpu_temperature
from .reading import Reading


class Sensor(ABC):
    def __init__(self, device_uuid: str):
        super().__init__()
        self.device_uuid = device_uuid

    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def model(self) -> MODEL:
        pass

    @property
    @abstractmethod
    def metrics(self) -> List[METRIC]:
        pass

    @abstractmethod
    async def get_readings(self) -> List[Reading]:
        pass


class DHT22Sensor(Sensor):
    def __init__(self, device_uuid: str, pointer: DHT22, pin: Pin):
        super().__init__(device_uuid)
        self.pointer = pointer
        self.pin = pin

    @property
    def id(self) -> str:
        return f"pin{self.pin}"

    @property
    def model(self) -> MODEL:
        return MODEL.DHT22

    @property
    def metrics(self) -> List[METRIC]:
        return [METRIC.TEMPERATURE, METRIC.HUMIDITY]

    def _get_metric_value(self, metric: METRIC) -> Optional[float]:
        try:
            if metric == METRIC.TEMPERATURE:
                return self.pointer.temperature
            return self.pointer.humidity
        except RuntimeError:
            # Reading DHT22 fails a lot...
            return None

    async def get_readings(self) -> List[Reading]:
        readings = []
        for metric in self.metrics:
            value = await run_in_executor(self._get_metric_value, metric)
            if value:
                readings.append(
                    Reading(self.device_uuid, self.model, self.id, metric, value)
                )
            await asyncio.sleep(2)
        return readings


def create_dht22_sensor(device_uuid: str, pin: int) -> DHT22Sensor:
    pin = Pin(pin)
    return DHT22Sensor(device_uuid, DHT22(pin), pin)


class DS18B20Sensor(Sensor):
    def __init__(self, device_uuid: str, pointer: W1ThermSensor):
        super().__init__(device_uuid)
        self.pointer = pointer

    @property
    def id(self) -> str:
        return self.pointer.id

    @property
    def model(self) -> MODEL:
        return MODEL.DS18B20

    @property
    def metrics(self) -> List[METRIC]:
        return [METRIC.TEMPERATURE]

    async def get_readings(self) -> List[Reading]:
        value = await run_in_executor(self.pointer.get_temperature)
        return [
            Reading(self.device_uuid, self.model, self.id, METRIC.TEMPERATURE, value)
        ]


def discover_ds18b20_sensors(device_uuid: str) -> List[DS18B20Sensor]:
    return [
        DS18B20Sensor(device_uuid, pointer)
        for pointer in W1ThermSensor.get_available_sensors()
    ]


class CPUSensor(Sensor):
    @property
    def id(self) -> str:
        return "cpu"

    @property
    def model(self) -> MODEL:
        return MODEL.CPU

    @property
    def metrics(self) -> List[METRIC]:
        return [METRIC.TEMPERATURE]

    async def get_readings(self) -> List[Reading]:
        value = await run_in_executor(get_cpu_temperature)
        return [
            Reading(self.device_uuid, self.model, self.id, METRIC.TEMPERATURE, value)
        ]


def create_cpu_sensor(device_uuid: str) -> CPUSensor:
    return CPUSensor(device_uuid)


class SensorCollection:
    def __init__(self, device_uuid: str, pins: Optional[List[int]] = None):
        self.cpu_collection = [create_cpu_sensor(device_uuid)]
        self.ds18b20_collection = discover_ds18b20_sensors(device_uuid)
        self.dht22_collection = (
            [create_dht22_sensor(device_uuid, pin) for pin in pins] if pins else []
        )
        self._lookup = {
            **{sensor.id: sensor for sensor in self.cpu_collection},
            **{sensor.id: sensor for sensor in self.ds18b20_collection},  # type: ignore
            **{sensor.id: sensor for sensor in self.dht22_collection},  # type: ignore
        }

    def keys(self):
        return list(self._lookup.keys())

    def __getitem__(self, sensor_id: str):
        return self._lookup[sensor_id]

    def __iter__(self):
        yield from self.cpu_collection
        yield from self.ds18b20_collection
        yield from self.dht22_collection
