from enum import Enum


class MODEL(Enum):
    CPU = "CPU"
    DHT22 = "DHT22"
    DS18B20 = "DS18B20"
    RELAY = "RELAY"


class METRIC(Enum):
    TEMPERATURE = "TEMPERATURE"
    HUMIDITY = "HUMIDITY"
    GPIO = "GPIO"
