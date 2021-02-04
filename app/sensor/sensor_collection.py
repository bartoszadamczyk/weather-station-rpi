import time

from w1thermsensor import W1ThermSensor
import adafruit_dht

from .sensor import Sensor, MODEL


class SensorCollection:
    def __init__(self, pins=None):
        self.sensors = []
        self._discover_ds18b20_sensors()
        if pins:
            self._generate_dht22_sensors(pins)

    def _discover_ds18b20_sensors(self):
        for pointer in W1ThermSensor.get_available_sensors():
            self.sensors.append(Sensor(pointer, MODEL.DS18B20))

    def _generate_dht22_sensors(self, pins):
        for pin in pins:
            self.sensors.append(Sensor(adafruit_dht.DHT22(pin), MODEL.DHT22, pin))

    def get_all_readings(self):
        readings = []
        for sensor in self.sensors:
            readings.append(sensor.get_reading())
            if sensor.model == MODEL.DHT22:
                time.sleep(2)
        return readings
