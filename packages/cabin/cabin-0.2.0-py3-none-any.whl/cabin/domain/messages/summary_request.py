from datetime import datetime

from cabin.domain.schema_type import SchemaType
from cabin.domain.summary_timespan import SummaryTimespan
from cabin.domain.tables.device import Device
from marshmallow_dataclass import dataclass


@dataclass
class SummaryRequest(SchemaType):
    """A request for a summary across all devices.
    A summary contains the average depth reading for a device over a given
    timespan. It is inserted into the DeviceTelemetry table.
    """

    timespan: SummaryTimespan
    startTime: datetime
    endTime: datetime


@dataclass
class DeviceSummaryRequest(SchemaType):
    """A summary request for a specific device.
    Contains parameter values used by the Function to collect the raw data to
    summarise.
    """

    timespan: SummaryTimespan
    device: Device
    startTimestamp: int
    endTimestamp: int
    readPartition: str
    writePartition: str
