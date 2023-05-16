from sqlalchemy import String, cast

from app.core.exceptions import BadRequest
from app.models import AuthUser

from .base import CRUDBase


class CRUDAuthUser(CRUDBase[AuthUser]):
    def get_by_email(self, email: str, with_: list | None = None) -> AuthUser:
        query = self._queryable(with_)
        query = query.filter(AuthUser.email == email)

        auth_user = query.first()

        return auth_user

    def get_students(self, with_: list | None = None) -> AuthUser:
        query = self._queryable(with_)
        query = query.filter(AuthUser.account_type == "student")

        return query.all()

    def get_wardens(self, with_: list | None = None) -> AuthUser:
        query = self._queryable(with_)
        query = query.filter(AuthUser.account_type == "warden")

        return query.all()

    def get_wardens_by_hostel_type(self, hostel_type: str) -> list[AuthUser]:
        query = self._queryable(None)
        query = query.filter(
            cast(AuthUser.hostel_details["type"], String) == hostel_type
        )

        return query.all()
