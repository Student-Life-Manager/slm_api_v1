from app.models import VerificationCode

from .base import CRUDBase


class CRUDVerificationCode(CRUDBase[VerificationCode]):
    def get_by_phone_number(self, phone_number: str) -> VerificationCode:
        return (
            self.db.query(VerificationCode)
            .filter(VerificationCode.phone_number == phone_number)
            .first()
        )