import json
import boto3

sqs = boto3.client("sqs")


def send_message_to_sqs(queue_url: str, message: dict):
    return sqs.send_message(
        QueueUrl=queue_url, MessageBody=json.dumps(message, default=str)
    )
