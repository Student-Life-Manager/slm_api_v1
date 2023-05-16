from datetime import datetime, timezone
from uuid import UUID

from app.core.exceptions import BadRequest, Forbidden
from app.crud import CRUDAuthUser, CRUDOutpass
from app.models import AuthUser, Outpass
from app.schema import OutpassCreate, OutpassUpdate
from app.schema.outpass import OutpassApproval, OutpassStatus

from .base import BaseController


class OutpassController(BaseController[OutpassCreate, OutpassUpdate]):
    def __init__(self, db, crud_outpass: CRUDOutpass):
        super().__init__(model=Outpass, db=db, crud_instance=crud_outpass)
        self.crud_outpass = crud_outpass

    def create(
        self,
        auth_user: AuthUser,
        outpass_create: OutpassCreate,
        warden_id: int,
        guardian_id: int,
    ) -> Outpass:
        active_outpasses = self.crud_outpass.get_all_active_outpasses_by_student_id(
            auth_user.id
        )
        print("active outpasses", active_outpasses)
        if len(active_outpasses) >= 5:
            raise Forbidden("A student cannot have more than 5 outpasses.")
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

        attributes = {"approval": approval, "approved_at": datetime.now(timezone.utc)}

        return self.crud_outpass.update(outpass, attributes)

    def get_outpass_by_student_id_and_uuid(
        self, student_id: int, uuid: UUID
    ) -> Outpass:
        return self.crud_outpass.get_outpass_by_student_id_and_uuid(
            student_id=student_id, uuid=uuid
        )

    def update_outpass_status(self, outpass: Outpass, status: OutpassStatus) -> Outpass:
        attributes = {}

        if status == OutpassStatus.REJECTED and outpass.status == OutpassStatus.CREATED:
            attributes["status"] = OutpassStatus.REJECTED.value
        elif status == OutpassStatus.REJECTED:
            raise BadRequest("Cannot reject an outpass after it has been accepted.")

        match status:
            case OutpassStatus.IN_CAMPUS:
                attributes["status"] = OutpassStatus.IN_CAMPUS.value

            case OutpassStatus.EXITED_CAMPUS:
                attributes["status"] = OutpassStatus.EXITED_CAMPUS.value
                attributes["exited_at"] = datetime.now(timezone.utc)

            case OutpassStatus.RETURNED_TO_CAMPUS:
                attributes["status"] = OutpassStatus.RETURNED_TO_CAMPUS.value
                attributes["returned_at"] = datetime.now(timezone.utc)

            case _:
                raise BadRequest("Incorrect outpass status value.")

        return self.crud_outpass.update(outpass, attributes)

    def get_student_outpasses(self, student_id: int) -> list[Outpass]:
        return self.crud_outpass.get_student_outpasses(student_id)

    def get_warden_outpasses(self, warden_id: int) -> list[Outpass]:
        return self.crud_outpass.get_warden_outpasses(warden_id)

    def get_warden_approved_outpasses(self, warden_id: int) -> list[Outpass]:
        return self.crud_outpass.get_warden_approved_outpasses(warden_id)
