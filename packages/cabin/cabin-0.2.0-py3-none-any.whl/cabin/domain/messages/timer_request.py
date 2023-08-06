from datetime import datetime

from marshmallow_dataclass import dataclass
from cabin.domain.schema_type import SchemaType


@dataclass
class ScheduleStatus:
    """Represents a timer schedule status.
    This isn't currently in the Python SDK
    (see: https://github.com/Azure/azure-functions-python-worker/issues/681) but
    it is in the raw JSON.

    - Last: Last recorded schedule occurrence
    - Next: Expected next schedule occurrence
    - LastUpdated: The last time this record was updated. This is used to
      re-calculate Next with the current Schedule after a host restart.
    """

    Last: datetime
    Next: datetime
    LastUpdated: datetime


@dataclass
class Schedule:
    AdjustForDST: bool


@dataclass
class TimerRequest(SchemaType):
    """A more complete version of the TimerRequest."""

    Schedule: Schedule
    ScheduleStatus: ScheduleStatus
    IsPastDue: bool
