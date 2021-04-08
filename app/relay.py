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
        self._pin = pin
        self._state = 0
        self._is_active = False
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

    async def init(self):
        if self._is_active:
            return
        print("Init for one relay started")
        self._state = 0
        self._is_active = True
        await run_in_executor(
            functools.partial(
                GPIO.setup,
                data={
                    "channel": self._pin,
                    "mode": GPIO.OUT,
                    "initial": GPIO.HIGH,
                },
            )
        )
        await self._callback(self._get_reading(METRIC_TYPE.INIT))

    async def up(self):
        if self._is_active and self._state == 0:
            self._state = 1
            await run_in_executor(GPIO.output, self._pin, GPIO.LOW)
            await self._callback(self._get_reading(METRIC_TYPE.CHANGE))

    async def down(self):
        if self._is_active and self._state == 1:
            self._state = 0
            await run_in_executor(GPIO.output, self._pin, GPIO.HIGH)
            await self._callback(self._get_reading(METRIC_TYPE.CHANGE))

    async def cleanup(self):
        print("In Clean up")
        if self._is_active:
            print("in active")
            self._is_active = False
            self._state = 0
            await run_in_executor(GPIO.cleanup, self._pin)
            print("cleaned one GPIO")
            await self._callback(self._get_reading(METRIC_TYPE.CLEANUP))
            print("sent metric about clean up")

    @property
    def component_id(self) -> str:
        return f"pin{self._pin}"

    @property
    def component_type(self) -> COMPONENT_TYPE:
        return COMPONENT_TYPE.RELAY

    @property
    def supported_metrics(self) -> List[METRIC_TYPE]:
        return [METRIC_TYPE.STATE]

    def _get_reading(self, metric: METRIC_TYPE):
        return Reading(self.component_type, self.component_id, metric, self._state)

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

    async def init(self):
        print("Manual init started")
        for rely in self:
            await rely.init()

    async def cleanup(self):
        print("Manual cleanup started")
        for rely in self:
            print("Manual cleanup for 1")
            await rely.cleanup()


def cleanup_gpio():
    print("Cleaning up gpio")
    GPIO.cleanup()
