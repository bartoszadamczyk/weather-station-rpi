from datetime import datetime
import unittest

from app.helper import get_timestamp, get_iso_date


class TestHelper(unittest.TestCase):
    def test_correctly_formats_timestamp(self):
        test_date = datetime(2020, 2, 20, 20, 20, 20, 123456)
        self.assertEqual(get_timestamp(test_date), 1582230020123)

    def test_correctly_formats_iso_date(self):
        test_date = datetime(2020, 2, 20, 20, 20, 20, 123456)
        self.assertEqual(get_iso_date(test_date), "2020-02-20T20:20:20.123")
