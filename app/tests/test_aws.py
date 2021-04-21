import unittest
from unittest.mock import patch, Mock

from app.aws import SQSClient


class TestSQSClient(unittest.TestCase):
    @patch("boto3.client")
    def test_it_works(self, client_mock):
        sqs_mock = Mock()
        client_mock.return_value = sqs_mock
        client = SQSClient()
        client_mock.assert_called_with("sqs")
        client.send_message_to_sqs("url", {"foo": "bar"})
        sqs_mock.send_message.assert_called_with(
            QueueUrl="url", MessageBody='{"foo": "bar"}'
        )

    @patch("boto3.client")
    @patch("botocore.exceptions.EndpointConnectionError")
    def test_handles_connection_error(self, error_mock, client_mock):
        sqs_mock = Mock()
        client_mock.return_value = sqs_mock
        client = SQSClient()
        client_mock.assert_called_with("sqs")
        sqs_mock.send_message.side_effect = error_mock
        client.send_message_to_sqs("url", {"foo": "bar"})
