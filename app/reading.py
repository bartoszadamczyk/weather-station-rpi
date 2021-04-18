from datetime import datetime, timezone

from .constants import MODULE_TYPE, METRIC_TYPE


class Reading:
    def __init__(
        self,
        module_type: MODULE_TYPE,
        module_id: str,
        metric_type: METRIC_TYPE,
        metric_value: float,
    ):
        self.created_on = datetime.now(tz=timezone.utc)
        self.module_type = module_type
        self.module_id = module_id
        self.metric_type = metric_type
        self.metric_value = metric_value

    @property
    def timestamp(self):
        return int(self.created_on.timestamp() * 1000)

    @property
    def iso_date(self):
        return self.created_on.isoformat()[:23]

    def __str__(self):
        return (
            f"{self.iso_date} {self.module_type.value} "
            f"{self.module_id} {self.metric_type.value} {self.metric_value:.2f}"
        )

    def as_dict(self):
        return {
            "created_on": self.timestamp,
            "module_type": self.module_type.value,
            "module_id": self.module_id,
            "metric_type": self.metric_type.value,
            "metric_value": self.metric_value,
        }
