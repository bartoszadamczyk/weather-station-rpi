from .async_handler import run_in_executor
from .aws import send_message_to_sqs
from .constants import ACTION_TYPE
from .reading import Reading


class ReadingsLogger:
    count = 0

    async def consume_reading(self, reading: Reading):
        if self.count < 200 or self.count % 100 < 10:
            print(reading)
        self.count += 1
        if self.count >= 1000000:
            self.count = 1000


class LiveSQSConsumer:
    def __init__(self, device_id: str, queue_url: str):
        self.device_id = device_id
        self.queue_url = queue_url
        self.base = {"action": ACTION_TYPE.LIVE_READING.value, "device_id": device_id}

    async def consume_reading(self, reading: Reading):
        body = {**self.base, **reading.as_dict()}
        await run_in_executor(send_message_to_sqs, self.queue_url, body)
