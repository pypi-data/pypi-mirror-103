from cabin.domain.tables.table_schema import TableSchema
from marshmallow_dataclass import dataclass


@dataclass
class User(TableSchema):
    """The schema for the User table."""

    role: str
    customerID: str

    @classmethod
    def new(cls, role: str, customerID: str):
        """Creates a new User object, automatically generating values for
        PartitionKey & RowKey.

        Args:
        - role: The customer's role, which determines their permissions. Also
            used as the PartitionKey.
        - customerID: The customer ID. Also used as the RowKey.

        Returns: A new User object.
        """
        return cls(
            PartitionKey=role,
            RowKey=customerID,
            role=role,
            customerID=customerID,
        )
