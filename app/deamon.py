import time

from graceful_killer import GracefulKiller
from relay import RelayCollection, cleanup_gpio
from sensor import SensorCollection

sensor_pins = [17, 27]
sensor_collection = SensorCollection(sensor_pins)

print("Test Sensors")
for sensor in sensor_collection:
    sensor = sensor_collection[sensor.name]
    print(sensor.get_reading())

print("Test Relays")
relay_pins = [26, 20, 21]
relay_collection = RelayCollection(relay_pins)
for relay in relay_collection:
    relay = relay[relay.pin]
    relay.up()

killer = GracefulKiller()
while not killer.kill_now:
    print("Start")
    for reading in sensor_collection.get_all_readings():
        print(reading)
    if not killer.kill_now:
        print("Sleep")
        time.sleep(3)

print("Done")
cleanup_gpio()
