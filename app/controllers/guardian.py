from uuid import UUID

from app.core.exceptions import BadRequest, Forbidden, NotFound
from app.crud.guardian import CRUDGuardian
from app.crud.outpass import CRUDOutpass
from app.models import Guardian
from app.schema.guardian import GuardianCreate, GuardianReturn, GuardianUpdate

from .base import BaseController


class GuardianController(BaseController[Guardian, GuardianUpdate]):
    def __init__(self, db, crud_guardian: CRUDGuardian, crud_outpass: CRUDOutpass):
        super().__init__(model=Guardian, db=db, crud_instance=crud_guardian)
        self.crud_guardian = crud_guardian
        self.crud_outpass = crud_outpass

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
        attributes["student_id"] = student_id

        return self.crud_guardian.create(attributes=attributes)

    def verify_guardian(self, guardian_uuid: UUID) -> Guardian:
        guardian = self.crud_guardian.get_by_uuid(guardian_uuid)

        if not guardian:
            raise NotFound("Guardian not found.")

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

        guardian = self.crud_guardian.get_guardian_with_uuid_and_student_id(
            student_id=student_id, uuid=guardian_uuid
        )
        if not guardian:
            raise NotFound("Guardian not found")

        self.crud_guardian.delete(guardian)

        return True

    def get_guardian_by_student_id_and_phone_number(
        self, student_id: int, phone_number: str
    ) -> Guardian:
        return self.crud_guardian.get_guardian_by_student_id_and_phone_number(
            student_id=student_id, phone_number=phone_number
        )

    def get_guardians(self) -> list[Guardian]:
        return self.crud_guardian.get_multi()
