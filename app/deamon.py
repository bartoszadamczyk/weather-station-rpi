import time

from alarm import Alarm, ALARM_TYPE, AlarmCollection
from graceful_killer import GracefulKiller
from relay import RelayCollection, cleanup_gpio
from sensor import METRIC, SensorCollection

try:
    sensor_pins = [17, 27]
    sensor_collection = SensorCollection(sensor_pins)

    relay_pins = [26, 20, 21]
    relay_collection = RelayCollection(relay_pins)

    alarm_collection = AlarmCollection()
    for i, sensor in enumerate(sensor_collection):
        pin = relay_pins[i]
        if not pin:
            break
        alarm_collection.add_alarm(
            Alarm(
                ALARM_TYPE.WARM_UP,
                sensor,
                METRIC.TEMPERATURE,
                relay_collection[relay_pins[i]],
                23,
                26,
            )
        )

    killer = GracefulKiller()
    while not killer.kill_now:
        print("Start")
        for sensor in sensor_collection:
            reading = sensor.get_reading()
            if reading:
                print(reading)
        if not killer.kill_now:
            for alarm in alarm_collection:
                alarm.check()
        if not killer.kill_now:
            print("Sleep")
            time.sleep(3)

except Exception:
    cleanup_gpio()
    raise

print("Done")
cleanup_gpio()
