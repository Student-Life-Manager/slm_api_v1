from datetime import date, datetime, time
from enum import Enum
from typing import ClassVar
from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel

from .generic import GenericReturn


class OutpassStatus(str, Enum):
    CREATED = "created"
    CONFIRMED = "confirmed"
    LIVE = "live"
    LATE = "late"
    CANCELLED = "cancelled"


class OutpassCreate(BaseModel):
    out_date: date
    out_time: time
    expected_return_at: date
    location: str
    reason: str
    alternate_phone_number: str | None = None


class OutpassUpdate(BaseModel):
    out_date: date | None = None
    out_time: time | None = None
    expected_return_at: date | None = None
    location: str | None = None
    reason: str | None = None
    alternate_phone_number: str | None = None


class OutpassReturn(GenericReturn):
    uuid: UUID
    out_date: date
    out_time: time
    expected_return_at: date
    location: str
    reason: str
    alternate_phone_number: str | None
    status: OutpassStatus
    approved_at: datetime | None
    exited_at: datetime | None
    returned_at: datetime | None
    warden_message: str | None
    approval: dict


class OutpassApproval(BaseModel):
    warden_1: bool = False
    warden_2: bool = False
