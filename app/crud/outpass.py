from uuid import UUID

from sqlalchemy import String, cast, or_
from sqlalchemy.orm import Query, joinedload

from app.models import Outpass
from app.schema.outpass import OutpassStatus

from .base import CRUDBase


class CRUDOutpass(CRUDBase[Outpass]):
    def get_student_outpasses(self, student_id: int, with_: list | None = None):
        query = self._queryable(with_)
        query = query.filter(Outpass.student_id == student_id)
        query = query.order_by(Outpass.out_time.desc())

        return query.all()

    def get_warden_outpasses(
        self, warden_id: int, with_: list | None = None
    ) -> list[Outpass]:
        query = self._queryable(with_)
        query = query.filter(Outpass.warden_id == warden_id)

        return query.all()

    def get_outpass_by_student_id_and_uuid(
        self, student_id: int, uuid: UUID, with_: list | None = None
    ) -> Outpass:
        query = self._queryable(with_)
        query = query.filter(Outpass.student_id == student_id)
        query = query.filter(Outpass.uuid == uuid)

        return query.first()

    def get_warden_approved_outpasses(
        self, warden_id: int, with_: list | None = None
    ) -> list[Outpass]:
        query = self._queryable(with_)
        query = query.filter(
            cast(Outpass.approval["warden_1"], String) == str(warden_id)
        )

        return query.all()

    def get_active_outpass_by_student_id(self, student_id: int) -> Outpass:
        self.db.query(Outpass).filter(Outpass.student_id == student_id).filter(
            Outpass.status == "exited_campus"
        ).first()

    def get_all_active_outpasses_by_student_id(self, student_id: int) -> list[Outpass]:
        return (
            self.db.query(Outpass)
            .filter(Outpass.student_id == student_id)
            .filter(
                or_(
                    Outpass.status == OutpassStatus.CREATED,
                    Outpass.status == OutpassStatus.IN_CAMPUS,
                    Outpass.status == OutpassStatus.EXITED_CAMPUS,
                )
            )
            .all()
        )

    def _with_student(self, query: Query):
        return query.options(joinedload(Outpass.student))

    def _with_guardian(self, query: Query):
        return query.options(joinedload(Outpass.guardian))
