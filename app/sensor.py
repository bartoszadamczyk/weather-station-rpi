from typing import Optional, List

from adafruit_dht import DHT22  # type: ignore
from adafruit_blinka.microcontroller.bcm283x.pin import Pin  # type: ignore
from w1thermsensor import W1ThermSensor  # type: ignore
from busio import I2C  # type: ignore
import adafruit_bme680  # type: ignore
import board  # type: ignore

from .async_handler import run_in_executor, Producer
from .constants import COMPONENT_TYPE, METRIC_TYPE
from .helper import get_cpu_temperature
from .reading import Reading


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
        if metric != METRIC_TYPE.TEMPERATURE:
            return None
        value = await run_in_executor(get_cpu_temperature)
        return Reading(self.component_type, self.component_id, metric, value)


def create_cpu_sensor() -> CPUSensor:
    return CPUSensor()


class DHT22Sensor(Producer):
    def __init__(self, pointer: DHT22, pin: Pin):
        super().__init__()
        self._pointer = pointer
        self._pin = pin

    @property
    def component_id(self) -> str:
        return f"pin{self._pin}"

    @property
    def component_type(self) -> COMPONENT_TYPE:
        return COMPONENT_TYPE.DHT22

    @property
    def supported_metrics(self) -> List[METRIC_TYPE]:
        return [METRIC_TYPE.TEMPERATURE, METRIC_TYPE.HUMIDITY]

    def _get_metric_value(self, metric: METRIC_TYPE) -> Optional[float]:
        try:
            if metric == METRIC_TYPE.TEMPERATURE:
                return self._pointer.temperature
            if metric == METRIC_TYPE.HUMIDITY:
                return self._pointer.humidity
            return None
        except RuntimeError:
            # Reading DHT22 fails a lot...
            return None

    async def get_reading(self, metric: METRIC_TYPE) -> Optional[Reading]:
        if metric not in self.supported_metrics:
            return None
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
        self._pointer = pointer

    @property
    def component_id(self) -> str:
        return self._pointer.id

    @property
    def component_type(self) -> COMPONENT_TYPE:
        return COMPONENT_TYPE.DS18B20

    @property
    def supported_metrics(self) -> List[METRIC_TYPE]:
        return [METRIC_TYPE.TEMPERATURE]

    async def get_reading(self, metric: METRIC_TYPE) -> Optional[Reading]:
        if metric != METRIC_TYPE.TEMPERATURE:
            return None
        value = await run_in_executor(self._pointer.get_temperature)
        return Reading(self.component_type, self.component_id, metric, value)


def discover_ds18b20_sensors() -> List[DS18B20Sensor]:
    return [DS18B20Sensor(pointer) for pointer in W1ThermSensor.get_available_sensors()]


class BME680Sensor(Producer):
    def __init__(self):
        super().__init__()
        self._i2c = I2C(board.SCL, board.SDA)
        self._pointer = adafruit_bme680.Adafruit_BME680_I2C(self._i2c)

    @property
    def component_id(self) -> str:
        return "bme680"

    @property
    def component_type(self) -> COMPONENT_TYPE:
        return COMPONENT_TYPE.BME680

    @property
    def supported_metrics(self) -> List[METRIC_TYPE]:
        return [
            METRIC_TYPE.TEMPERATURE,
            METRIC_TYPE.HUMIDITY,
            METRIC_TYPE.PRESSURE,
            METRIC_TYPE.GAS,
        ]

    def _get_metric_value(self, metric: METRIC_TYPE) -> Optional[float]:
        if metric == METRIC_TYPE.TEMPERATURE:
            return self._pointer.temperature
        if metric == METRIC_TYPE.HUMIDITY:
            return self._pointer.humidity
        if metric == METRIC_TYPE.PRESSURE:
            return self._pointer.pressure
        if metric == METRIC_TYPE.GAS:
            return self._pointer.gas
        return None

    async def get_reading(self, metric: METRIC_TYPE) -> Optional[Reading]:
        if metric not in self.supported_metrics:
            return None
        value = await run_in_executor(self._get_metric_value, metric)
        if value:
            return Reading(self.component_type, self.component_id, metric, value)
        return None


def create_bme680_sensor() -> BME680Sensor:
    return BME680Sensor()
