from app.async_handler import run_in_executor
from app.aws import SQSClient
from app.constants import ACTION_TYPE
from app.reading import Reading


class ReadingsLogger:
    def __init__(
        self,
        init_window_size: int = 200,
        log_window_size: int = 10,
        skip_window_size: int = 500,
        logger=print,
    ):
        self.count = 0
        self.init_window_size = init_window_size
        self.log_window_size = log_window_size
        self.skip_window_size = skip_window_size
        self.logger = logger

    async def consume_reading(self, reading: Reading):
        if self.count < self.init_window_size + self.log_window_size:
            self.logger(reading)
        self.count += 1
        if (
            self.count
            >= self.init_window_size + self.log_window_size + self.skip_window_size
        ):
            if self.log_window_size and self.skip_window_size:
                self.logger(f"Skipped {self.skip_window_size} readings")
            self.count = self.init_window_size


class LiveSQSConsumer:
    def __init__(self, sqs_client: SQSClient, device_id: str, queue_url: str):
        self.sqs_client = sqs_client
        self.device_id = device_id
        self.queue_url = queue_url
        self.base = {"action": ACTION_TYPE.LIVE_READING.value, "device_id": device_id}

    async def consume_reading(self, reading: Reading):
        body = {**self.base, **reading.as_dict()}
        await run_in_executor(self.sqs_client.send_message_to_sqs, self.queue_url, body)
