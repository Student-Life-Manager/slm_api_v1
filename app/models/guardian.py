from uuid import uuid4

from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

from app.database.setup import Base


class Guardian(Base):
    __tablename__ = "guardian"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, nullable=False)
    relation = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)

    student_id = Column(BigInteger, ForeignKey("auth_user.id"), nullable=False)
    student = relationship(
        "AuthUser", back_populates="guardians", uselist=False, lazy="raise"
    )

    created_at = Column(DateTime, nullable=False, default=func.now())

    __table_args__ = (Index("idx__guardian_student_id", student_id),)
