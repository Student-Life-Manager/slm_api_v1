from uuid import UUID

from sqlalchemy import String, cast, or_

from app.models import Outpass

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
            or_(
                cast(Outpass.approval["warden_1"], String) == str(warden_id),
                cast(Outpass.approval["warden_2"], String) == str(warden_id),
            )
        )

        return query.all()
