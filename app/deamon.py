import time

from aws import send_message_to_sqs
from .alarm import ALARM_TYPE, Alarm, AlarmCollection
from .graceful_killer import GracefulKiller
from .relay import cleanup_gpio, RelayCollection
from .reading import METRIC
from .sensor import SensorCollection


def run():
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
                    relay_collection[pin],
                    23,
                    26,
                )
            )

        killer = GracefulKiller()
        while not killer.kill_now:
            for sensor in sensor_collection:
                reading = sensor.get_reading()
                if reading:
                    print(reading)
                    try:
                        send_message_to_sqs(reading)
                    except Exception:
                        print("Failed to send reading to sqs")

            if not killer.kill_now:
                for alarm in alarm_collection:
                    alarm.check()
            if not killer.kill_now:
                time.sleep(3)

    except Exception:
        cleanup_gpio()
        raise

    print("Done")
    cleanup_gpio()
