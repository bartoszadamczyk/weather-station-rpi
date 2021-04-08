from datetime import datetime, timezone

from .constants import MODEL, METRIC


class Reading:
    def __init__(
        self,
        sensor_model: MODEL,
        sensor_id: str,
        metric: METRIC,
        value: float,
    ):
        self.datetime = datetime.now(tz=timezone.utc)
        self.sensor_model = sensor_model
        self.sensor_id = sensor_id
        self.metric = metric
        self.value = value

    @property
    def timestamp(self):
        return int(self.datetime.timestamp() * 1000)

    @property
    def iso_date(self):
        return self.datetime.isoformat()[:23]

    def __str__(self):
        return (
            f"{self.iso_date} {self.metric.value} "
            f"{self.sensor_model.value} {self.sensor_id} {self.value:.2f}"
        )

    def as_dict(self):
        return {
            "datetime": self.timestamp,
            "sensor_model": self.sensor_model.value,
            "sensor_id": self.sensor_id,
            "metric": self.metric.value,
            "value": self.value,
        }
