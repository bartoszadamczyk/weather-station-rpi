from enum import Enum


class COMPONENT_TYPE(Enum):
    CPU = "cpu"
    DHT22 = "dht22"
    DS18B20 = "ds18b20"
    BME680 = "bme680"

    RELAY = "relay"


class METRIC_TYPE(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    GAS = "gas"

    INIT = "init"
    STATE = "state"
    CHANGE = "change"
    CLEANUP = "cleanup"
