from datetime import datetime
from unittest.mock import Mock

import pytest
from aiounittest import AsyncTestCase

from app.consumer import LiveSQSConsumer, ReadingsLogger
from app.constants import MODULE_TYPE, METRIC_TYPE
from app.helper import get_timestamp
from app.reading import Reading


class TestLiveSQSConsumer(AsyncTestCase):
    @pytest.mark.asyncio
    async def test_it_works(self):
        test_date = datetime(2020, 2, 20, 20, 20, 20, 123456)
        test_date_timestamp = get_timestamp(test_date)
        sqs_client = Mock()
        consumer = LiveSQSConsumer(sqs_client, "device_id", "queue_url")
        reading = Reading(
            MODULE_TYPE.RPI, "cpu", METRIC_TYPE.TEMPERATURE, 10.12345, test_date
        )
        await consumer.consume_reading(reading)
        correct_dict = {
            "action": "live_reading",
            "device_id": "device_id",
            "created_on": test_date_timestamp,
            "module_type": "rpi",
            "module_id": "cpu",
            "metric_type": "temperature",
            "metric_value": 10.12345,
        }
        sqs_client.send_message_to_sqs.assert_called_with("queue_url", correct_dict)


class TestReadingsLogger(AsyncTestCase):
    reading = Reading(MODULE_TYPE.RPI, "cpu", METRIC_TYPE.TEMPERATURE, 10.12345)

    @pytest.mark.asyncio
    async def test_it_works(self):
        logger_mock = Mock()
        consumer = ReadingsLogger(10, 20, 30, logger=logger_mock)

        # init window
        for i in range(10):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 10)

        # log window
        for i in range(20):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 30)

        # skip window
        for i in range(29):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 30)

        # skip window ends
        await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 31)

        # log window
        for i in range(20):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 51)

        # skip window
        for i in range(29):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 51)

        # skip window ends
        await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 52)

        # log window
        for i in range(20):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 72)

    @pytest.mark.asyncio
    async def test_it_works_without_init_window(self):
        logger_mock = Mock()
        consumer = ReadingsLogger(0, 20, 30, logger=logger_mock)

        # log window
        for i in range(20):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 20)

        # skip window
        for i in range(29):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 20)

        # skip window ends
        await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 21)

        # log window
        for i in range(20):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 41)

        # skip window
        for i in range(29):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 41)

        # skip window ends
        await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 42)

        # log window
        for i in range(20):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 62)

    @pytest.mark.asyncio
    async def test_it_works_without_log_window(self):
        logger_mock = Mock()
        consumer = ReadingsLogger(10, 0, 30, logger=logger_mock)

        # init window
        for i in range(10):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 10)

        # log window
        for i in range(200):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 10)

    @pytest.mark.asyncio
    async def test_it_works_without_skip_window(self):
        logger_mock = Mock()
        consumer = ReadingsLogger(10, 20, 0, logger=logger_mock)

        # init window
        for i in range(10):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 10)

        # log window
        for i in range(200):
            await consumer.consume_reading(self.reading)
        self.assertEqual(logger_mock.call_count, 210)
