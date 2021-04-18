import json
import os

"""
To override BALENA_DEVICE_UUID, provide:
- DEVICE_ID

To enable Sentry, provide:
- SENTRY_DSN = string
- SENTRY_ENVIRONMENT = string

To enable DHT22 sensors, provide:
- DHT22_PINS = [17]

To enable BME680 sensor, provide:
- ENABLE_BME680 = True

To enable Relays, provide:
- RELAY_PINS = [26,20,21]

To enable LiveSQSConsumer, provide:
- AWS_ACCESS_KEY_ID = string
- AWS_SECRET_ACCESS_KEY = string
- AWS_DEFAULT_REGION = string
- AWS_SQS_DATA = string
"""

_DEVICE_ID = os.getenv("DEVICE_ID")
_DHT22_PINS = os.getenv("DHT22_PINS")
_RELAY_PINS = os.getenv("RELAY_PINS")


class CONFIG:
    DEVICE_ID = _DEVICE_ID if _DEVICE_ID else os.environ["BALENA_DEVICE_UUID"]

    # Optional
    DHT22_PINS = json.loads(_DHT22_PINS) if _DHT22_PINS else None
    ENABLE_BME680 = True if os.getenv("ENABLE_BME680") else False
    RELAY_PINS = json.loads(_RELAY_PINS) if _RELAY_PINS else None
    AWS_SQS_DATA = os.getenv("AWS_SQS_DATA")
