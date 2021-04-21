from enum import Enum


class ACTION_TYPE(Enum):
    LIVE_READING = "live_reading"


class MODULE_TYPE(Enum):
    RPI = "rpi"
    DHT22 = "dht22"
    DS18B20 = "ds18b20"
    BME680 = "bme680"
    RELAY = "relay"


class METRIC_TYPE(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    VOX = "vox"
    STATE = "state"
