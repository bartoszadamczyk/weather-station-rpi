import time

from microcontroller import Pin  # type: ignore

from sensor.sensor_collection import SensorCollection

pins = [Pin(17), Pin(27)]


sensors = SensorCollection(pins)

while True:
    print("Start")
    for reading in sensors.get_all_readings():
        print(reading)
        time.sleep(3)
