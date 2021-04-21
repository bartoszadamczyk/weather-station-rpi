import os

from app.config import Config


def _load_config_from_environment():
    balena_device_uuid = os.getenv("BALENA_DEVICE_UUID")
    device_id = os.getenv("DEVICE_ID")
    dht22_pins = os.getenv("DHT22_PINS")
    enable_bme680 = os.getenv("ENABLE_BME680")
    relay_pins = os.getenv("RELAY_PINS")
    aws_sqs_data = os.getenv("AWS_SQS_DATA")
    return Config(
        balena_device_uuid=balena_device_uuid,
        device_id=device_id,
        dht22_pins=dht22_pins,
        enable_bme680=enable_bme680,
        relay_pins=relay_pins,
        aws_sqs_data=aws_sqs_data,
    )


CONFIG = _load_config_from_environment()
