from datetime import datetime
from typing import Any, Dict

import cabin.utils.time as time_utils
from cabin.domain.schema_type import SchemaType
from cabin.domain.tables.table_schema import TableSchema
from marshmallow_dataclass import dataclass


@dataclass
class SensorData(SchemaType):
    """The readings from the device sensors.

    Fields:
    - humidity (float): The measured humidity as a percentage
    - temperature (float): The temperature reading (°C)
    - timestamp (str): The time that the readings were taken.
        Stored in a second-based Unix timestamp.
    """

    humidity: float
    temperature: float
    timestamp: int


@dataclass
class DeviceTelemetry(TableSchema):
    """The schema for the DeviceTelemetry table.
    Stores raw readings from devices.
    """

    customerID: str
    deviceID: str
    sensorData: SensorData
    messageCount: int
    version: str
    insertTimestamp: int

    @classmethod
    def new(
        cls,
        customerID: str,
        deviceID: str,
        messageCount: int,
        version: str,
        sensorData: Dict[str, Any],
    ):  # -> DeviceTelemetry:
        """Creates a new DeviceTelemetry object, automatically generating values
        for PartitionKey, RowKey, and insertTimestamp.

        Args: Values for class fields (excluding PartitionKey & RowKey).

        Returns: A new DeviceTelemetry object.
        """
        sensor_data = SensorData(**sensorData)
        return cls(
            PartitionKey=cls.partition_key(customerID, deviceID),
            RowKey=str(sensor_data.timestamp),
            customerID=customerID,
            deviceID=deviceID,
            sensorData=sensor_data,
            messageCount=messageCount,
            version=version,
            insertTimestamp=time_utils.timestamp(datetime.utcnow()),
        )

    @staticmethod
    def partition_key(customerID: str, deviceID: str) -> str:
        """Creates the partition key for a DeviceTelemetry row.

        Args:
        - customerID: The customer ID.
        - deviceID: The device ID.

        Returns: The partition key.
        """
        return f"{customerID}_{deviceID}"

    @staticmethod
    def row_key(dt: datetime) -> str:
        """Formats a datetime into a timestamp for use as a RowKey.

        Args:
        - dt: The datetime that the message was received.

        Returns: A Unix timestamp in second precision.
        """
        return str(time_utils.timestamp(dt))
