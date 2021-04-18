import json
import boto3
from botocore.exceptions import EndpointConnectionError


class SQSClient:
    def __init__(self):
        self.sqs = boto3.client("sqs")

    def send_message_to_sqs(self, queue_url: str, message: dict):
        try:
            return self.sqs.send_message(
                QueueUrl=queue_url, MessageBody=json.dumps(message, default=str)
            )
        except EndpointConnectionError:
            print("Failed to connect to the SQS endpoint. Are we offline?")
