from .async_handler import run_in_executor
from .aws import SQSClient
from .constants import ACTION_TYPE
from .reading import Reading


class ReadingsLogger:
    count = 0

    async def consume_reading(
        self,
        reading: Reading,
        initWindowSize: int = 200,
        logWindowSize: int = 10,
        skipWindowSize: int = 1000,
    ):
        if self.count < 210:
            print(reading)
        self.count += 1
        if self.count >= 710:
            print("Skipped 500 readings")
            self.count = 200


class LiveSQSConsumer:
    def __init__(self, sqs_client: SQSClient, device_id: str, queue_url: str):
        self.sqs_client = sqs_client
        self.device_id = device_id
        self.queue_url = queue_url
        self.base = {"action": ACTION_TYPE.LIVE_READING.value, "device_id": device_id}

    async def consume_reading(self, reading: Reading):
        body = {**self.base, **reading.as_dict()}
        await run_in_executor(self.sqs_client.send_message_to_sqs, self.queue_url, body)
