from enum import Enum


class COMPONENT_TYPE(Enum):
    CPU = "cpu"
    DHT22 = "dht22"
    DS18B20 = "ds18b20"

    RELAY = "relay"


class METRIC_TYPE(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"

    INIT = "init"
    STATE = "state"
    CHANGE = "change"
    CLEANUP = "cleanup"
