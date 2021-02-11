import time

from graceful_killer import GracefulKiller
from relay import Relay, cleanup_gpio
from sensor import SensorCollection

pins = [17, 27]
sensors = SensorCollection(pins)

pins = [26, 20, 21]
relay = Relay(26)

killer = GracefulKiller()
while not killer.kill_now:
    print("Start")
    relay.up()
    for reading in sensors.get_all_readings():
        if not killer.kill_now:
            print(reading)
    time.sleep(3)

cleanup_gpio()
