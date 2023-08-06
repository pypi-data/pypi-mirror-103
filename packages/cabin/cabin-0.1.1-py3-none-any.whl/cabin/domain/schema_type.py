from typing import ClassVar, Type

from marshmallow import Schema


class SchemaType:
    """Base class for marshmallow dataclasses. Adds Schema field."""

    Schema: ClassVar[Type[Schema]] = Schema
