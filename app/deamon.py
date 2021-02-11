import time


from sensor.sensor_collection import SensorCollection

pins = [17, 27]


sensors = SensorCollection(pins)

while True:
    print("Start")
    for reading in sensors.get_all_readings():
        print(reading)
        time.sleep(3)
