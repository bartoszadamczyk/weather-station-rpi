from abc import ABC, abstractmethod
from typing import Union, Optional, List

from adafruit_dht import DHT22  # type: ignore
from adafruit_blinka.microcontroller.bcm283x.pin import Pin  # type: ignore
from w1thermsensor import W1ThermSensor  # type: ignore

from .reading import Reading
from .reading_collection import ReadingCollection


class Sensor(ABC):
    def __init__(self, pointer: Union[DHT22, W1ThermSensor]):
        super().__init__()
        self.pointer = pointer
        self.reading_collection = ReadingCollection()

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_reading(self) -> Optional[Reading]:
        pass


class DHT22Sensor(Sensor):
    def __init__(self, pointer: Union[DHT22, W1ThermSensor], pin: Pin):
        super().__init__(pointer)
        self.pin = pin

    @property
    def name(self) -> str:
        return "dht22_{}" % self.pin

    def get_reading(self) -> Optional[Reading]:
        try:
            reading = Reading(self.pointer.temperature, self.pointer.humidity)
        except RuntimeError:
            # Reading DHT22 fails a lot...
            return None
        self.reading_collection.add_reading(reading)
        return reading


def create_dht22_sensor(pin: int) -> DHT22Sensor:
    pin = Pin(pin)
    return DHT22Sensor(DHT22(pin), pin)


class DS18B20Sensor(Sensor):
    @property
    def name(self):
        return "ds18b20_{}" % self.pointer.id

    def get_reading(self) -> Reading:
        reading = Reading(self.pointer.get_temperature())
        self.reading_collection.add_reading(reading)
        return reading


def discover_ds18b20_sensors() -> List[DS18B20Sensor]:
    return [DS18B20Sensor(pointer) for pointer in W1ThermSensor.get_available_sensors()]
