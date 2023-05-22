from datetime import date, datetime, time
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from .auth_user import AuthUserBasicReturn, AuthUserReturn
from .generic import GenericReturn
from .guardian import GuardianReturn


class OutpassStatus(str, Enum):
    CREATED = "created"
    REJECTED = "rejected"
    IN_CAMPUS = "in_campus"
    EXITED_CAMPUS = "exited_campus"
    RETURNED_TO_CAMPUS = "returned_to_campus"
    LATE_RETURN = "late_return"


class OutpassCreate(BaseModel):
    out_date: date
    out_time: time | None = None
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


class OutpassApproval(BaseModel):
    warden_1: str | None = None
    warden_2: str | None = None


class OutpassRejectionDetails(BaseModel):
    warden_1: str | None = None
    warden_2: str | None = None


class OutpassReturn(GenericReturn):
    uuid: UUID
    out_date: date
    out_time: time | None = None
    expected_return_at: date
    location: str
    reason: str
    alternate_phone_number: str | None
    status: OutpassStatus
    approved_at: datetime | None
    exited_at: datetime | None
    returned_at: datetime | None
    warden_message: str | None
    approval: OutpassApproval
    rejection: OutpassRejectionDetails

    class Config:
        orm_mode = True


class OutpassWithStudentReturn(OutpassReturn):
    student: AuthUserBasicReturn


class OutpassWithGuardianAndWardenReturn(OutpassReturn):
    warden: AuthUserReturn
    guardian: GuardianReturn


class OutpassRejection(BaseModel):
    warden_message: str


class OutpassStatusChange(BaseModel):
    status: OutpassStatus
