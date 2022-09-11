from datetime import datetime
from uuid import UUID

from tortoise import Model
from tortoise.fields import (
    DatetimeField,
    IntField,
    UUIDField,
    FloatField,
    SmallIntField,
)


class StatsEntry(Model):
    """A single entry in the stats table."""

    id: int = IntField(pk=True)
    created_on: datetime = DatetimeField(null=False, auto_now_add=True)
    manga_uuid: UUID = UUIDField(null=False, index=True)
    chapter_num: float = FloatField(null=False)
    pages: int = SmallIntField(null=False)
    bytes: int = IntField(null=False)
