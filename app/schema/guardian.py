from typing import ClassVar
from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, EmailStr

from .generic import GenericReturn


class GuardianCreate(BaseModel):
    relation: str
    phone_number: str


class GuardianUpdate(BaseModel):
    relation: str | None = None
    phone_number: str | None = None


class GuardianReturn(GenericReturn):
    uuid: UUID
    relation: str
    phone_number: str
    is_verified: bool

    class Config:
        orm_mode = True

class AddGuardiansWithStudentEmail(BaseModel):
    Email: str
    Relation: str
    Phone: str