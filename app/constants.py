from enum import Enum


class MODEL(Enum):
    CPU = "cpu"
    DHT22 = "dht22"
    DS18B20 = "ds18b20"
    RELAY = "relay"


class METRIC(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    GPIO = "gpio"
    STATE = "state"
    CHANGE = "change"
