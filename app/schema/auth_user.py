from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, validator

from app.core.config import settings

from .generic import GenericReturn
from .guardian import GuardianReturn
from .outpass import OutpassReturn

phone_number = "123456"
MAX_NUMBER_OF_USERS = 123

# primitive types: int, str, float. boolean
# boolean: True or False
# str: "1", "A", "B", "C"

# AuthUserAccountType: "student", "warden", "admin"


class AuthUserAccountType(str, Enum):
    STUDENT = "student"
    WARDEN = "warden"
    ADMIN = "admin"


class HostelType(str, Enum):
    BOYS = "boys"
    GIRLS = "girls"


class StudentAcademicDetails(BaseModel):
    year_of_study: int | None = None
    course: str | None = None
    branch: str | None = None
    section: str | None = None


class AuthUserHostelDetails(BaseModel):
    hostel_type: HostelType | None = None
    bldg_name: str | None = None
    room_no: str | None = None


class StudentCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: str

    @validator("email")
    def validate_email_domain(cls, email):
        if not email.endswith(settings.ALLOWED_EMAIL_DOMAIN):
            raise ValueError("Invalid email.")

        return email


class WardenCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone_number: str
    hostel_details: AuthUserHostelDetails


class AuthUserLogin(BaseModel):
    email: EmailStr
    password: str


class AuthUserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    roll_number: str | None = None
    phone_number: str | None = None
    hostel_details: AuthUserHostelDetails | None = None
    academic_details: StudentAcademicDetails | None = None


class AuthUserAuthRefresh(BaseModel):
    access_token: str
    refresh_token: str


class AuthUserTokenReturn(BaseModel):
    access_token: str
    refresh_token: str


class StudentChecklist(BaseModel):
    personal_details: bool = False
    hostel_details: bool = False
    academic_details: bool = False


class WardenChecklist(BaseModel):
    personal_details: bool = False
    hostel_details: bool = False


class AuthUserPasswordUpdate(BaseModel):
    password: str


class StudentRegisterReturn(BaseModel):
    email: str
    phone_number: str

    class Config:
        orm_mode = True


class AuthUserBasicReturn(GenericReturn):
    uuid: UUID
    first_name: str
    last_name: str
    roll_number: str
    email: str

    class Config:
        orm_mode = True


class AuthUserReturn(AuthUserBasicReturn):
    account_type: AuthUserAccountType
    phone_number: str
    roll_number: str
    email: EmailStr
    phone_number: str
    hostel_details: AuthUserHostelDetails
    academic_details: StudentAcademicDetails

    class Config:
        orm_mode = True


class AuthUserWithGuardiansReturn(AuthUserReturn):
    guardians: list[GuardianReturn]


class AuthUserHomeReturn(BaseModel):
    auth_user: AuthUserBasicReturn
    outpass: list[OutpassReturn]
