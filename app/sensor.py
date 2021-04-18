from typing import Optional, List

from adafruit_dht import DHT22  # type: ignore
from adafruit_blinka.microcontroller.bcm283x.pin import Pin  # type: ignore
from w1thermsensor import W1ThermSensor, SensorNotReadyError  # type: ignore
from busio import I2C  # type: ignore
import adafruit_bme680  # type: ignore
import board  # type: ignore

from .async_handler import run_in_executor, Producer
from .constants import MODULE_TYPE, METRIC_TYPE
from .helper import get_cpu_temperature
from .reading import Reading


class RPISensor(Producer):
    @property
    def module_id(self) -> str:
        return "cpu"

    @property
    def module_type(self) -> MODULE_TYPE:
        return MODULE_TYPE.RPI

    @property
    def supported_metric_types(self) -> List[METRIC_TYPE]:
        return [METRIC_TYPE.TEMPERATURE]

    async def get_reading(self, metric_type: METRIC_TYPE) -> Optional[Reading]:
        if metric_type != METRIC_TYPE.TEMPERATURE:
            return None
        metric_value = await run_in_executor(get_cpu_temperature)
        return Reading(self.module_type, self.module_id, metric_type, metric_value)


def create_rpi_sensor() -> RPISensor:
    return RPISensor()


class DHT22Sensor(Producer):
    def __init__(self, pointer: DHT22, pin: Pin):
        super().__init__()
        self._pointer = pointer
        self._pin = pin

    @property
    def module_id(self) -> str:
        return f"pin{self._pin}"

    @property
    def module_type(self) -> MODULE_TYPE:
        return MODULE_TYPE.DHT22

    @property
    def supported_metric_types(self) -> List[METRIC_TYPE]:
        return [METRIC_TYPE.TEMPERATURE, METRIC_TYPE.HUMIDITY]

    def _get_metric_value(self, metric_type: METRIC_TYPE) -> Optional[float]:
        try:
            if metric_type == METRIC_TYPE.TEMPERATURE:
                return self._pointer.temperature
            if metric_type == METRIC_TYPE.HUMIDITY:
                return self._pointer.humidity
            return None
        except RuntimeError:
            # Reading DHT22 fails a lot...
            return None

    async def get_reading(self, metric_type: METRIC_TYPE) -> Optional[Reading]:
        if metric_type not in self.supported_metric_types:
            return None
        metric_value = await run_in_executor(self._get_metric_value, metric_type)
        if metric_value:
            return Reading(self.module_type, self.module_id, metric_type, metric_value)
        return None


def create_dht22_sensor(pin: int) -> DHT22Sensor:
    pin = Pin(pin)
    return DHT22Sensor(DHT22(pin), pin)


class DS18B20Sensor(Producer):
    def __init__(self, pointer: W1ThermSensor):
        super().__init__()
        self._pointer = pointer

    @property
    def module_id(self) -> str:
        return self._pointer.id

    @property
    def module_type(self) -> MODULE_TYPE:
        return MODULE_TYPE.DS18B20

    @property
    def supported_metric_types(self) -> List[METRIC_TYPE]:
        return [METRIC_TYPE.TEMPERATURE]

    def _get_metric_value(self, metric_type: METRIC_TYPE) -> Optional[float]:
        try:
            if metric_type == METRIC_TYPE.TEMPERATURE:
                return self._pointer.get_temperature()
            return None
        except SensorNotReadyError:
            print("Failed to read from DS18B20, check your wires")
            return None

    async def get_reading(self, metric_type: METRIC_TYPE) -> Optional[Reading]:
        if metric_type not in self.supported_metric_types:
            return None
        metric_value = await run_in_executor(self._get_metric_value, metric_type)
        return Reading(self.module_type, self.module_id, metric_type, metric_value)


def discover_ds18b20_sensors() -> List[DS18B20Sensor]:
    return [DS18B20Sensor(pointer) for pointer in W1ThermSensor.get_available_sensors()]


class BME680Sensor(Producer):
    def __init__(self):
        super().__init__()
        self._i2c = I2C(board.SCL, board.SDA)
        self._pointer = adafruit_bme680.Adafruit_BME680_I2C(self._i2c)

    @property
    def module_id(self) -> str:
        # Until not tested for more than one, this is going to be hardcoded
        return "0x77"

    @property
    def module_type(self) -> MODULE_TYPE:
        return MODULE_TYPE.BME680

    @property
    def supported_metric_types(self) -> List[METRIC_TYPE]:
        return [
            METRIC_TYPE.TEMPERATURE,
            METRIC_TYPE.HUMIDITY,
            METRIC_TYPE.PRESSURE,
            METRIC_TYPE.GAS,
        ]

    def _get_metric_value(self, metric_type: METRIC_TYPE) -> Optional[float]:
        try:
            if metric_type == METRIC_TYPE.TEMPERATURE:
                return self._pointer.temperature
            if metric_type == METRIC_TYPE.HUMIDITY:
                return self._pointer.humidity
            if metric_type == METRIC_TYPE.PRESSURE:
                return self._pointer.pressure
            if metric_type == METRIC_TYPE.GAS:
                return self._pointer.gas
            return None
        except OSError:
            print("Failed to read from BME680, check your wires")
            return None

    async def get_reading(self, metric_type: METRIC_TYPE) -> Optional[Reading]:
        if metric_type not in self.supported_metric_types:
            return None
        metric_value = await run_in_executor(self._get_metric_value, metric_type)
        if metric_value:
            return Reading(self.module_type, self.module_id, metric_type, metric_value)
        return None


def create_bme680_sensor() -> BME680Sensor:
    return BME680Sensor()
