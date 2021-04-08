import os

from .async_handler import AsyncHandler
from .consumers import ReadingsLogger, LiveSQSConsumer
from .relay import RelayHandler, cleanup_gpio
from .sensor import (
    create_cpu_sensor,
    discover_ds18b20_sensors,
    create_dht22_sensor,
)

DEVICE_UUID = os.environ["BALENA_DEVICE_UUID"]

DEFAULT_CONFIG = {
    "CPU": True,
    "DHT22": [17],
    "DS18B20": True,
    "BME689": False,
    "RELAY": [26, 20, 21],
}

CONFIG = DEFAULT_CONFIG


def run():
    async_handler = AsyncHandler()

    # Create sensors
    if CONFIG["CPU"]:
        async_handler.add_producer(create_cpu_sensor())
    if CONFIG["DHT22"]:
        for pin in CONFIG["DHT22"]:
            async_handler.add_producer(create_dht22_sensor(pin), 1, 2)
    if CONFIG["DS18B20"]:
        for sensor in discover_ds18b20_sensors():
            async_handler.add_producer(sensor)

    # Create relays
    if CONFIG["RELAY"]:
        relay_collection = RelayHandler(CONFIG["RELAY"])
        for relay in relay_collection:
            async_handler.add_producer(relay, 60, delay=60)
        async_handler.run_in_loop(relay_collection.init)
        async_handler.add_cleanup(relay_collection.cleanup)

    # Create consumers
    async_handler.add_consumer(ReadingsLogger())

    queue_url = os.getenv("AWS_SQS_DATA")
    if queue_url:
        async_handler.add_consumer(LiveSQSConsumer(DEVICE_UUID, queue_url))
    try:
        async_handler.start()
    finally:
        cleanup_gpio()


# Manual relay trigger
# Way for alarm to call relay
# TODO: siterm


# def run():
#     try:
#         relay_pins = [26, 20, 21]
#         relay_collection = RelayCollection(relay_pins)
#
#         alarm_collection = AlarmCollection()
#         for i, sensor in enumerate(sensor_collection):
#             pin = relay_pins[i]
#             if not pin:
#                 break
#             alarm_collection.add_alarm(
#                 Alarm(
#                     ALARM_TYPE.WARM_UP,
#                     sensor,
#                     METRIC.TEMPERATURE,
#                     relay_collection[pin],
#                     23,
#                     26,
#                 )
#             )
#
#         killer = GracefulKiller()
#         while not killer.kill_now:
#             for sensor in sensor_collection:
#                 reading = sensor.get_reading()
#                 if reading:
#                     print(reading)
#                     send_message_to_sqs(reading.as_dict())
#             if not killer.kill_now:
#                 for alarm in alarm_collection:
#                     alarm.check()
#             if not killer.kill_now:
#                 time.sleep(3)
#
#     except Exception:
#         cleanup_gpio()
#         raise
#
#     print("Done")
#     cleanup_gpio()
