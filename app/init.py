
from .async_handler import AsyncHandler
from .config import CONFIG
from .consumers import ReadingsLogger, LiveSQSConsumer
from .relay import RelayHandler, cleanup_gpio
from .sensor import (
    create_rpi_sensor,
    discover_ds18b20_sensors,
    create_dht22_sensor,
    create_bme680_sensor,
)



def run():
    async_handler = AsyncHandler()

    # Create sensors
    async_handler.add_producer(create_rpi_sensor())
    if CONFIG.DHT22_PINS:
        for pin in CONFIG.DHT22_PINS:
            async_handler.add_producer(create_dht22_sensor(pin), 1, 2)
    for sensor in discover_ds18b20_sensors():
        async_handler.add_producer(sensor)
    if CONFIG.ENABLE_BME680:
        async_handler.add_producer(create_bme680_sensor())

    # Create relays
    if CONFIG.RELAY_PINS:
        relay_collection = RelayHandler(CONFIG.RELAY_PINS)
        for relay in relay_collection:
            async_handler.add_producer(relay, 60, delay=60)
        async_handler.run_in_loop(relay_collection.init)
        async_handler.add_cleanup(relay_collection.cleanup)

    # Create consumers
    async_handler.add_consumer(ReadingsLogger())
    if CONFIG.AWS_SQS_DATA:
        async_handler.add_consumer(
            LiveSQSConsumer(CONFIG.DEVICE_ID, CONFIG.AWS_SQS_DATA)
        )

    # Start the app
    try:
        async_handler.start()
    finally:
        cleanup_gpio()
