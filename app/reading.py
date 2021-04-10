from datetime import datetime, timezone

from .constants import COMPONENT_TYPE, METRIC_TYPE


class Reading:
    def __init__(
        self,
        component_type: COMPONENT_TYPE,
        component_id: str,
        metric: METRIC_TYPE,
        value: float,
    ):
        self.created_on = datetime.now(tz=timezone.utc)
        self.component_type = component_type
        self.component_id = component_id
        self.metric = metric
        self.value = value

    @property
    def timestamp(self):
        return int(self.created_on.timestamp() * 1000)

    @property
    def iso_date(self):
        return self.created_on.isoformat()[:23]

    def __str__(self):
        return (
            f"{self.iso_date} {self.component_type.value} "
            f"{self.component_id} {self.metric.value} {self.value:.2f}"
        )

    def as_dict(self):
        return {
            "created_on": self.timestamp,
            "component_type": self.component_type.value,
            "component_id": self.component_id,
            "metric": self.metric.value,
            "value": self.value,
        }
