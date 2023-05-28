from random import randint
from uuid import UUID

from app.core.exceptions import BadRequest, Forbidden, NotFound
from app.crud.guardian import CRUDGuardian
from app.crud.outpass import CRUDOutpass
from app.crud.verification_code import CRUDVerificationCode
from app.models import AuthUser, Guardian, VerificationCode
from app.schema.guardian import GuardianCreate, GuardianReturn, GuardianUpdate
from app.services import TwilioService

from .base import BaseController


class GuardianController(BaseController[Guardian, GuardianUpdate]):
    def __init__(
        self,
        db,
        crud_guardian: CRUDGuardian,
        crud_outpass: CRUDOutpass,
        crud_verification_code: CRUDVerificationCode,
        twilio_service: TwilioService,
    ):
        super().__init__(model=Guardian, db=db, crud_instance=crud_guardian)
        self.crud_guardian = crud_guardian
        self.crud_outpass = crud_outpass
        self.crud_verification_code = crud_verification_code
        self.twilio_service = twilio_service

    def create(
        self,
        guardian_create: GuardianCreate,
        student_id: int,
    ) -> GuardianReturn:
        guardian = self.crud_guardian.get_guardian_by_student_id_and_relation(
            student_id=student_id, relation=guardian_create.relation
        )
        if guardian:
            raise BadRequest("Guardian with this relation already exists.")

        guardian = self.crud_guardian.get_guardian_by_student_id_and_phone_number(
            student_id=student_id, phone_number=guardian_create.phone_number
        )

        if guardian:
            raise BadRequest("Guardian with this phone number already exists.")

        attributes = self.extract_attributes_from_schema(guardian_create)
        attributes["phone_number"] = "+91" + guardian_create.phone_number
        attributes["student_id"] = int(student_id)

        return self.crud_guardian.create(attributes=attributes)

    def send_guardian_verification_message(
        self,
        auth_user: AuthUser,
        guardian: Guardian,
    ) -> VerificationCode:
        verification_code = self._assign_otp_to_guardian(
            phone_number=guardian.phone_number,
            auth_user_name=f"{auth_user.first_name} {auth_user.last_name}",
        )

        return verification_code

    def verify_guardian(self, guardian_uuid: UUID, code: str) -> Guardian:
        guardian = self.crud_guardian.get_by_uuid(guardian_uuid)

        if not guardian:
            raise NotFound("Guardian not found.")

        assigned_verification_code = self.crud_verification_code.get_by_phone_number(
            guardian.phone_number
        )

        if not assigned_verification_code:
            raise BadRequest("No assigned otp for guardian.")

        if assigned_verification_code.code != code:
            raise BadRequest("Incorrect code.")

        attributes = {"is_verified": True}

        return self.crud_guardian.update(guardian, attributes)

    def get_student_guardians(self, student_id: int) -> list[GuardianReturn]:
        return self.crud_guardian.get_student_guardians(student_id)

    def get_guardian_by_student_id_and_relation(
        self, student_id: int, relation: str, with_: list | None = None
    ) -> Guardian:
        return self.crud_guardian.get_guardian_by_student_id_and_relation(
            student_id=student_id, relation=relation, with_=with_
        )

    def delete(self, student_id: int, guardian_uuid: UUID) -> bool:
        active_outpass = self.crud_outpass.get_active_outpass_by_student_id(student_id)

        if active_outpass:
            raise Forbidden("Cannot delete guardians while an outpass is active")

        guardian = self.crud_guardian.get_guardian_with_student_id_and_uuid(
            student_id=student_id, uuid=guardian_uuid
        )
        if not guardian:
            raise NotFound("Guardian not found")

        self.crud_guardian.delete(guardian)

        return True

    def get_guardian_with_student_id_and_uuid(
        self, student_id: int, guardian_uuid: UUID
    ) -> Guardian:
        return self.crud_guardian.get_guardian_with_uuid_and_student_id(
            student_id=student_id, uuid=guardian_uuid
        )

    def get_guardian_by_student_id_and_phone_number(
        self, student_id: int, phone_number: str
    ) -> Guardian:
        return self.crud_guardian.get_guardian_by_student_id_and_phone_number(
            student_id=student_id, phone_number=phone_number
        )

    def get_guardians(self) -> list[Guardian]:
        return self.crud_guardian.get_multi()

    def _assign_otp_to_guardian(
        self, phone_number: str, auth_user_name: str
    ) -> VerificationCode:
        code = randint(100, 100000)

        existing_assigned_code = self.crud_verification_code.get_by_phone_number(
            phone_number
        )

        if existing_assigned_code:
            self.crud_verification_code.delete(existing_assigned_code)

        self.twilio_service.send_verification_message(
            phone_number=phone_number,
            message=f"Welcome! {auth_user_name} has added you as their guardian to Capstone App. Your verification code is: {code}.",
        )

        return self.crud_verification_code.create(
            {"code": code, "phone_number": phone_number}
        )