from pydantic import BaseModel

from .generic import GenericReturn


class VerificationCodeReturn(GenericReturn):
    code: str
    phone_number: str

    class Config:
        orm_mode = True