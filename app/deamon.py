from datetime import datetime
import time
from w1thermsensor import W1ThermSensor
import adafruit_dht
import board

pins = [board.D17, board.D27]


class MODEL:
    DHT22 = "DHT22"
    DS18B20 = "DS18B20"


class Reading:
    def __init__(self, sensor, temperature, humidity=None, now=None):
        self.sensor = sensor
        self.temperature = temperature
        self.humidity = humidity
        self.now = now if now else datetime.now()

    def __str__(self):
        if self.humidity:
            return "Sensor {} ID {} temperature {:.2f}C humidity {:.2f}%".format( self.sensor.model, self.sensor.id, self.temperature, self.humidity)
        return "Sensor {} ID {} temperature {:.2f}C".format(
            self.sensor.model, self.sensor.id, self.temperature
        )


class Sensor:
    def __init__(self, pointer, model, pin=None):
        self.pointer = pointer
        self.model = model
        self.id = pin if pin else pointer.id

    def get_reading(self):
        if self.model == MODEL.DS18B20:
            return Reading(self, self.pointer.get_temperature())
        if self.model == MODEL.DHT22:
            try:
                return Reading(self, self.pointer.temperature, self.pointer.humidity)
            except RuntimeError as error:
                print(error.args[0])
                return None


class Sensors:
    def __init__(self, pins):
        self.sensors = []
        self._discover_ds18b20_sensors()
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
            if sensor.model == MODEL.DHT22 and sensor != self.sensors[-1]:
                time.sleep(2)
        return readings


sensors = Sensors(pins)

while True:
    print("Start")
    for reading in sensors.get_all_readings():
        print(reading)
    time.sleep(1)
