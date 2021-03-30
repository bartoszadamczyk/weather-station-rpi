import json
import os

import boto3

sqs = boto3.client("sqs")

# This is going to throw if missing
QUEUE_URL = os.environ["AWS_SQS_DATA"]


def send_message_to_sqs(message: dict):
    return sqs.send_message(
        QueueUrl=QUEUE_URL, MessageBody=json.dumps(message, default=str)
    )
