import os

from .async_handler import AsyncHandler
from .consumers import ReadingsLogger, LiveSQSConsumer
from .relay import RelayHandler, cleanup_gpio
from .sensor import (
    create_cpu_sensor,
    discover_ds18b20_sensors,
    create_dht22_sensor,
    create_bme680_sensor,
)

DEVICE_UUID = os.environ["BALENA_DEVICE_UUID"]

DEFAULT_CONFIG = {
    "DHT22": [17],
    "RELAY": [26, 20, 21],
}

CONFIG = DEFAULT_CONFIG


def run():
    async_handler = AsyncHandler()

    # Create sensors
    async_handler.add_producer(create_cpu_sensor())
    for pin in CONFIG["DHT22"]:
        async_handler.add_producer(create_dht22_sensor(pin), 1, 2)
    for sensor in discover_ds18b20_sensors():
        async_handler.add_producer(sensor)
    if os.getenv("BME680"):
        async_handler.add_producer(create_bme680_sensor())

    # Create relays
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
