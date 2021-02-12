import time

from graceful_killer import GracefulKiller
from relay import RelayCollection, cleanup_gpio
from sensor import SensorCollection

try:
    sensor_pins = [17, 27]
    sensor_collection = SensorCollection(sensor_pins)

    relay_pins = [26, 20, 21]
    relay_collection = RelayCollection(relay_pins)

    # for relay in relay_collection:
    #     relay.up()

    killer = GracefulKiller()
    while not killer.kill_now:
        print("Start")
        for sensor in sensor_collection:
            print(f"{sensor.name} {sensor.get_reading()}")
        if not killer.kill_now:
            print("Sleep")
            time.sleep(3)

except Exception:
    cleanup_gpio()
    raise

print("Done")
cleanup_gpio()
