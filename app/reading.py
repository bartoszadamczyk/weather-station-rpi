from datetime import datetime, timezone

from .constants import MODEL, METRIC


class Reading:
    def __init__(
        self,
        device_uuid: str,
        sensor_model: MODEL,
        sensor_id: str,
        metric: METRIC,
        value: float,
    ):
        self.datetime = datetime.now(tz=timezone.utc)
        self.device_uuid = device_uuid
        self.sensor_model = sensor_model
        self.sensor_id = sensor_id
        self.metric = metric
        self.value = value

    def __str__(self):
        return f"{self.sensor_id} {self.metric.value} {self.value:.2f}"

    def as_dict(self):
        return {
            "datetime": int(self.datetime.timestamp() * 1000),
            "device_uuid": self.device_uuid,
            "sensor_model": self.sensor_model.value,
            "sensor_id": self.sensor_id,
            "metric": self.metric.value,
            "value": self.value,
        }
