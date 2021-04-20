from datetime import datetime
import unittest

from app.constants import MODULE_TYPE, METRIC_TYPE
from app.helper import get_timestamp, get_iso_date
from app.reading import Reading


class TestReading(unittest.TestCase):
    test_date = datetime(2020, 2, 20, 20, 20, 20, 123456)
    test_date_timestamp = get_timestamp(test_date)
    test_date_iso_date = get_iso_date(test_date)

    def test_correctly_formats_timestamp(self):
        reading = Reading(
            MODULE_TYPE.RPI, "cpu", METRIC_TYPE.TEMPERATURE, 10, self.test_date
        )
        self.assertEqual(reading.timestamp, self.test_date_timestamp)

    def test_correctly_formats_iso_date(self):
        reading = Reading(
            MODULE_TYPE.RPI, "cpu", METRIC_TYPE.TEMPERATURE, 10, self.test_date
        )
        self.assertEqual(reading.iso_date, self.test_date_iso_date)

    def test_correctly_formats_as_string(self):
        reading = Reading(
            MODULE_TYPE.RPI, "cpu", METRIC_TYPE.TEMPERATURE, 10.123, self.test_date
        )
        correct_output = (
            f"{self.test_date_iso_date} {MODULE_TYPE.RPI.value} cpu "
            f"{METRIC_TYPE.TEMPERATURE.value} 10.12"
        )
        self.assertEqual(reading.__str__(), correct_output)

    def test_correctly_formats_as_dict(self):
        test_value = 10.123
        reading = Reading(
            MODULE_TYPE.RPI, "cpu", METRIC_TYPE.TEMPERATURE, 10.123, self.test_date
        )
        correct_dict = {
            "created_on": self.test_date_timestamp,
            "module_type": MODULE_TYPE.RPI.value,
            "module_id": "cpu",
            "metric_type": METRIC_TYPE.TEMPERATURE.value,
            "metric_value": test_value,
        }
        self.assertEqual(reading.as_dict(), correct_dict)
