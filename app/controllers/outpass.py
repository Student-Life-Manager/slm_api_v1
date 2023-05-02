from uuid import UUID

from app.core.exceptions import BadRequest, Unauthorized
from app.crud import CRUDAuthUser, CRUDOutpass
from app.models import AuthUser, Outpass
from app.schema import OutpassCreate, OutpassUpdate
from app.schema.outpass import OutpassApproval, OutpassStatus

from .base import BaseController


class OutpassController(BaseController[OutpassCreate, OutpassUpdate]):
    def __init__(self, db, crud_outpass: CRUDOutpass):
        super().__init__(model=Outpass, db=db, crud_instance=crud_outpass)
        self.crud_outpass = crud_outpass

    def create(self, auth_user: AuthUser, outpass_create: OutpassCreate, warden_id : int, guardian_id : int) -> Outpass:
        attributes = self.extract_attributes_from_schema(outpass_create)
        attributes["student_id"] = auth_user.id
        attributes["warden_id"] = warden_id
        attributes["guardian_id"] = guardian_id
    
        attributes["status"] = OutpassStatus.CREATED

        if not hasattr(attributes, "approval"):
            attributes["approval"] = OutpassApproval().__dict__

        outpass = self.crud_outpass.create(attributes)

        return outpass

    def approve_first_level_outpass(
        self, warden: AuthUser, outpass: Outpass
    ) -> Outpass:
        approval = outpass.approval

        approval["warden_1"] = warden.id

        attributes = {"approval": approval}

        return self.crud_outpass.update(outpass, attributes)

    def get_outpass_by_student_id_and_uuid(
        self, student_id: int, uuid: UUID
    ) -> Outpass:
        return self.crud_outpass.get_outpass_by_student_id_and_uuid(
            student_id=student_id, uuid=uuid
        )

    def get_student_outpasses(self, student_id: int) -> list[Outpass]:
        return self.crud_outpass.get_student_outpasses(student_id)

    def get_warden_outpasses(self, warden_id: int) -> list[Outpass]:
        return self.crud_outpass.get_warden_outpasses(warden_id)

    def get_warden_approved_outpasses(self, warden_id: int) -> list[Outpass]:
        return self.crud_outpass.get_warden_approved_outpasses(warden_id)
