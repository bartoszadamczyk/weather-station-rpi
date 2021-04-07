import os

# import time
# from typing import Protocol, List

# import asyncio

# from .alarm import ALARM_TYPE, Alarm, AlarmCollection
from .async_handler import AsyncHandler

# from .aws import send_message_to_sqs
from .consumers import ReadingsLogger

# from .constants import METRIC
# from .helper import GracefulKiller
# from .reading import Reading
from .relay import cleanup_gpio
from .sensor import (
    create_cpu_sensor,
    discover_ds18b20_sensors,
    create_dht22_sensor,
)

BALENA_DEVICE_UUID = os.environ["BALENA_DEVICE_UUID"]

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
    async_handler.add_cleanup(cleanup_gpio)

    # Create sensors
    if CONFIG["CPU"]:
        async_handler.add_producer(create_cpu_sensor(BALENA_DEVICE_UUID))
    if CONFIG["DHT22"]:
        for pin in CONFIG["DHT22"]:
            async_handler.add_producer(create_dht22_sensor(BALENA_DEVICE_UUID, pin))
    if CONFIG["DS18B20"]:
        for sensor in discover_ds18b20_sensors(BALENA_DEVICE_UUID):
            async_handler.add_producer(sensor)

    async_handler.add_consumer(ReadingsLogger())

    async_handler.start()


# Using the aiofiles:
#
# async with aiofiles.open('filename', mode='r') as f:
#     async for line in f:
#         print(line)

# TODO: siterm
# await q.put(await asyncio.run_in_executor(None, bigcalculation))


# def run():
#     try:
#         sensor_pins = [17]
#         sensor_collection = SensorCollection(BALENA_DEVICE_UUID, sensor_pins)
#
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
