import functools
from typing import List, Optional

import RPi.GPIO as GPIO  # type: ignore

from .async_handler import Producer, run_in_executor
from .constants import COMPONENT_TYPE, METRIC_TYPE
from .reading import Reading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class Relay(Producer):
    def __init__(self, pin: int):
        super().__init__()
        self.pin = pin
        self.state = 0
        self.callback = None
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

    async def init(self):
        self.state = 0
        await run_in_executor(
            functools.partial(
                GPIO.setup,
                data={
                    "channel_or_chan_list": self.pin,
                    "mode": GPIO.OUT,
                    "initial": GPIO.HIGH,
                },
            )
        )
        await self.callback(self._get_reading(METRIC_TYPE.INIT))

    async def up(self):
        self.state = 1
        await run_in_executor(GPIO.output, self.pin, GPIO.LOW)
        await self.callback(self._get_reading(METRIC_TYPE.CHANGE))

    async def down(self):
        self.state = 0
        await run_in_executor(GPIO.output, self.pin, GPIO.HIGH)
        await self.callback(self._get_reading(METRIC_TYPE.CHANGE))

    async def cleanup(self):
        self.state = 0
        await run_in_executor(GPIO.cleanup, self.pin)
        await self.callback(self._get_reading(METRIC_TYPE.CLEANUP))

    @property
    def component_id(self) -> str:
        return f"pin{self.pin}"

    @property
    def component_type(self) -> COMPONENT_TYPE:
        return COMPONENT_TYPE.RELAY

    @property
    def supported_metrics(self) -> List[METRIC_TYPE]:
        return [METRIC_TYPE.STATE]

    def _get_reading(self, metric: METRIC_TYPE):
        return Reading(self.component_type, self.component_id, metric, self.state)

    async def get_reading(self, metric: METRIC_TYPE) -> Optional[Reading]:
        if metric in self.supported_metrics:
            return self._get_reading(metric)
        return None


class RelayHandler:
    def __init__(self, pins: List[int]):
        self._collection = []
        self._lookup = {}

        for pin in pins:
            relay = Relay(pin)
            self._collection.append(relay)
            self._lookup[pin] = relay

    def keys(self):
        return list(self._lookup.keys())

    def __getitem__(self, pin: int):
        return self._lookup[pin]

    def __iter__(self):
        yield from self._collection

    def init(self):
        [relay.init() for relay in self]

    def cleanup(self):
        [relay.cleanup() for relay in self]


def cleanup_gpio():
    print("Cleaning up gpio")
    GPIO.cleanup()
