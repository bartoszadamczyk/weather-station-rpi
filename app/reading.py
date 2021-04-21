from datetime import datetime, timezone

from app.constants import MODULE_TYPE, METRIC_TYPE
from app.helper import get_timestamp, get_iso_date


class Reading:
    def __init__(
        self,
        module_type: MODULE_TYPE,
        module_id: str,
        metric_type: METRIC_TYPE,
        metric_value: float,
        created_on: datetime = None,
    ):
        self.module_type = module_type
        self.module_id = module_id
        self.metric_type = metric_type
        self.metric_value = metric_value
        self.created_on = created_on or datetime.now(tz=timezone.utc)

    @property
    def timestamp(self):
        return get_timestamp(self.created_on)

    @property
    def iso_date(self):
        return get_iso_date(self.created_on)

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
