import unittest
from app.config import Config


class TestConfig(unittest.TestCase):
    def test_it_works_for_all_vars(self):
        config = Config(
            "BALENA_DEVICE_UUID", "DEVICE_ID", "[17]", "True", "[21]", "URL"
        )
        self.assertEqual(config.DEVICE_ID, "DEVICE_ID")
        self.assertEqual(config.DHT22_PINS, [17])
        self.assertEqual(config.ENABLE_BME680, True)
        self.assertEqual(config.RELAY_PINS, [21])
        self.assertEqual(config.AWS_SQS_DATA, "URL")

    def test_it_handles_missing_vars(self):
        config = Config("BALENA_DEVICE_UUID")
        self.assertEqual(config.DEVICE_ID, "BALENA_DEVICE_UUID")
        self.assertEqual(config.DHT22_PINS, None)
        self.assertEqual(config.ENABLE_BME680, False)
        self.assertEqual(config.RELAY_PINS, None)
        self.assertEqual(config.AWS_SQS_DATA, None)
