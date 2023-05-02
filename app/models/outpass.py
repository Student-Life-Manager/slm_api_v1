from uuid import uuid4

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    Time,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship

from app.database.setup import Base


class Outpass(Base):
    __tablename__ = "outpass"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, nullable=False)
    out_date = Column(Date, nullable=False)
    out_time = Column(Time, nullable=False)
    expected_return_at = Column(Date, nullable=False)
    location = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    alternate_phone_number = Column(String)
    status = Column(String, nullable=False)
    # possible statuses = [in_campus,exited_campus,returned_to_campus,late_return]
    # TODO : ADD THESE COLUMNS
    approved_at = Column(DateTime)
    exited_at = Column(DateTime)
    returned_at = Column(DateTime)
    warden_message = Column(String)
    # for first level and second level permissions
    approval = Column(MutableDict.as_mutable(JSONB), nullable=False)

    # Relationships with auth user table
    student_id = Column(BigInteger, ForeignKey("auth_user.id"), nullable=False)
    warden_id = Column(BigInteger, ForeignKey("auth_user.id"), nullable=False)
    student = relationship(
        "AuthUser",
        foreign_keys=[student_id],
        back_populates="outpasses",
        uselist=False,
    )
    guardian_id = Column(BigInteger, ForeignKey("guardian.id"), nullable=False)

    __table_args__ = (
        Index("idx__outpass_uuid", uuid),
        Index("idx__outpass_out_date", out_date),
        Index("idx__outpass_status", status),
    )
