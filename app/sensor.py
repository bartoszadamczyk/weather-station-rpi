from typing import Optional, List

from adafruit_dht import DHT22  # type: ignore
from adafruit_blinka.microcontroller.bcm283x.pin import Pin  # type: ignore
from w1thermsensor import W1ThermSensor  # type: ignore

from .async_handler import run_in_executor, Producer
from .constants import COMPONENT_TYPE, METRIC_TYPE
from .helper import get_cpu_temperature
from .reading import Reading


class DHT22Sensor(Producer):
    def __init__(self, pointer: DHT22, pin: Pin):
        super().__init__()
        self.pointer = pointer
        self.pin = pin

    @property
    def component_id(self) -> str:
        return f"pin{self.pin}"

    @property
    def component_type(self) -> COMPONENT_TYPE:
        return COMPONENT_TYPE.DHT22

    @property
    def supported_metrics(self) -> List[METRIC_TYPE]:
        return [METRIC_TYPE.TEMPERATURE, METRIC_TYPE.HUMIDITY]

    def _get_metric_value(self, metric: METRIC_TYPE) -> Optional[float]:
        try:
            if metric == METRIC_TYPE.TEMPERATURE:
                return self.pointer.temperature
            return self.pointer.humidity
        except RuntimeError:
            # Reading DHT22 fails a lot...
            return None

    async def get_reading(self, metric: METRIC_TYPE) -> Optional[Reading]:
        if metric in self.supported_metrics:
            value = await run_in_executor(self._get_metric_value, metric)
            if value:
                return Reading(self.component_type, self.component_id, metric, value)
        return None


def create_dht22_sensor(pin: int) -> DHT22Sensor:
    pin = Pin(pin)
    return DHT22Sensor(DHT22(pin), pin)


class DS18B20Sensor(Producer):
    def __init__(self, pointer: W1ThermSensor):
        super().__init__()
        self.pointer = pointer

    @property
    def component_id(self) -> str:
        return self.pointer.id

    @property
    def component_type(self) -> COMPONENT_TYPE:
        return COMPONENT_TYPE.DS18B20

    @property
    def supported_metrics(self) -> List[METRIC_TYPE]:
        return [METRIC_TYPE.TEMPERATURE]

    async def get_reading(self, metric: METRIC_TYPE) -> Optional[Reading]:
        if metric == METRIC_TYPE.TEMPERATURE:
            value = await run_in_executor(self.pointer.get_temperature)
            return Reading(self.component_type, self.component_id, metric, value)
        return None


def discover_ds18b20_sensors() -> List[DS18B20Sensor]:
    return [DS18B20Sensor(pointer) for pointer in W1ThermSensor.get_available_sensors()]


class CPUSensor(Producer):
    @property
    def component_id(self) -> str:
        return "cpu"

    @property
    def component_type(self) -> COMPONENT_TYPE:
        return COMPONENT_TYPE.CPU

    @property
    def supported_metrics(self) -> List[METRIC_TYPE]:
        return [METRIC_TYPE.TEMPERATURE]

    async def get_reading(self, metric: METRIC_TYPE) -> Optional[Reading]:
        if metric == METRIC_TYPE.TEMPERATURE:
            value = await run_in_executor(get_cpu_temperature)
            return Reading(self.component_type, self.component_id, metric, value)
        return None


def create_cpu_sensor() -> CPUSensor:
    return CPUSensor()
