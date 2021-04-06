import time
from abc import ABC, abstractmethod
from typing import Union, Optional, List

from adafruit_dht import DHT22  # type: ignore
from adafruit_blinka.microcontroller.bcm283x.pin import Pin  # type: ignore
from w1thermsensor import W1ThermSensor  # type: ignore

from .reading import ReadingCollection, Reading


class MODEL:
    CPU = "CPU"
    DHT22 = "DHT22"
    DS18B20 = "DS18B20"


class Sensor(ABC):
    def __init__(self, device_uuid: str):
        super().__init__()
        self.device_uuid = device_uuid
        self.reading_collection = ReadingCollection()

    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def model(self) -> str:
        pass

    @abstractmethod
    def get_reading(self, delay: int = 0) -> Optional[Reading]:
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
    def model(self) -> str:
        return MODEL.DHT22

    def get_reading(self, delay: int = 3) -> Optional[Reading]:
        time.sleep(delay)

        try:
            reading = Reading(
                self.device_uuid,
                self.id,
                self.model,
                self.pointer.temperature,
                self.pointer.humidity,
            )
        except RuntimeError:
            # Reading DHT22 fails a lot...
            return None
        self.reading_collection.add_reading(reading)
        return reading


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
    def model(self) -> str:
        return MODEL.DS18B20

    def get_reading(self, delay: int = 0) -> Reading:
        time.sleep(delay)
        reading = Reading(
            self.device_uuid, self.id, self.model, self.pointer.get_temperature()
        )
        self.reading_collection.add_reading(reading)
        return reading


def discover_ds18b20_sensors(
    device_uuid: str,
) -> List[DS18B20Sensor]:
    return [
        DS18B20Sensor(device_uuid, pointer)
        for pointer in W1ThermSensor.get_available_sensors()
    ]


class CPUSensor(Sensor):
    @property
    def id(self) -> str:
        return "cpu"

    @property
    def model(self) -> str:
        return MODEL.CPU

    def _get_cpu_temperature(self) -> float:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as cpu_temperature_file:
            return int(cpu_temperature_file.read()) / 1000

    def get_reading(self, delay: int = 0) -> Reading:
        time.sleep(delay)
        reading = Reading(
            self.device_uuid, self.id, self.model, self._get_cpu_temperature()
        )
        self.reading_collection.add_reading(reading)
        return reading


def create_cpu_sensor(
    device_uuid: str,
) -> CPUSensor:
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
