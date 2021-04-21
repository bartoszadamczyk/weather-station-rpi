import json
from typing import Optional

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


class MissingEnvVariableException(Exception):
    def __init__(self, var: str):
        self.var = var

    def __str__(self):
        return f"Missing Env Variable: {self.var}"


class Config:
    def __init__(
        self,
        balena_device_uuid: Optional[str],
        device_id: str = None,
        dht22_pins: str = None,
        enable_bme680: str = None,
        relay_pins: str = None,
        aws_sqs_data: str = None,
    ):
        if not balena_device_uuid:
            raise MissingEnvVariableException("BALENA_DEVICE_UUID")

        self.DEVICE_ID = device_id if device_id else balena_device_uuid
        self.DHT22_PINS = json.loads(dht22_pins) if dht22_pins else None
        self.ENABLE_BME680 = True if enable_bme680 else False
        self.RELAY_PINS = json.loads(relay_pins) if relay_pins else None
        self.AWS_SQS_DATA = aws_sqs_data or None
