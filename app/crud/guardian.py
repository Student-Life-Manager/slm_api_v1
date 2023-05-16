from uuid import UUID

from sqlalchemy.orm import Query, joinedload

from app.models.guardian import Guardian

from .base import CRUDBase


class CRUDGuardian(CRUDBase[Guardian]):
    def get_student_guardians(
        self, student_id: int, with_: list | None = None
    ) -> list[Guardian]:
        query = self._queryable(with_)
        query = query.filter(Guardian.student_id == student_id)

        return query.all()

    def get_guardian_with_uuid_and_student_id(
        self, student_id: int, uuid: UUID
    ) -> Guardian:
        return (
            self.db.query(Guardian)
            .filter(Guardian.student_id == student_id)
            .filter(Guardian.uuid == uuid)
            .first()
        )

    def get_guardian_by_student_id_and_relation(
        self, student_id: int, relation: str, with_: list | None = None
    ) -> Guardian:
        query = self._queryable(with_)
        query = query.filter(Guardian.student_id == student_id)
        query = query.filter(Guardian.relation == relation)
        return query.first()

    def get_guardian_by_student_id_and_phone_number(
        self,
        student_id: int,
        phone_number: str,
    ) -> Guardian:
        return (
            self.db.query(Guardian)
            .filter(Guardian.student_id == student_id)
            .filter(Guardian.phone_number == phone_number)
            .first()
        )

    def _with_student(self, query: Query) -> Query:
        return query.options(joinedload(Guardian.student))
