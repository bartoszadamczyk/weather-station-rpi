from relay import Relay
from sensor import Sensor


class ALARM_TYPE:
    WARM_UP = "WARM_UP"


class ALARM_STATUS:
    UP = "UP"
    DOWN = "DOWN"


class Alarm:
    def __init__(
        self,
        alarm_type: str,
        sensor: Sensor,
        metric: str,
        relay: Relay,
        start: float,
        stop: float,
        window_size: int = 5,
    ):
        self.alarm_type = alarm_type
        self.sensor = sensor
        self.metric = metric
        self.relay = relay
        self.start = start
        self.stop = stop
        self.window_size = window_size
        self.status = ALARM_STATUS.DOWN

    def check(self) -> str:
        metric_value = self.sensor.reading_collection.get_value(
            self.metric, self.window_size
        )
        if not metric_value:
            return self.status
        if self.status == ALARM_STATUS.UP and metric_value > self.stop:
            self.status = ALARM_STATUS.DOWN
            self.relay.down()
            print(
                f"Alarm for {self.sensor.name} has changed to DOWN:"
                " {metric_value} > {self.stop}"
            )
        if self.status == ALARM_STATUS.DOWN and metric_value < self.start:
            self.status = ALARM_STATUS.UP
            self.relay.up()
            print(
                f"Alarm for {self.sensor.name} has changed to UP:"
                " {metric_value} < {self.start}"
            )

        return self.status
