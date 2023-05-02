import datetime
from uuid import uuid4

# from .outpass import Outpass
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Index, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

from app.database.setup import Base

from .outpass import Outpass


class AuthUser(Base):
    __tablename__ = "auth_user"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    checklist = Column(MutableDict.as_mutable(JSONB), nullable=False)
    roll_number = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    account_type = Column(String)
    phone_number = Column(String)
    academic_details = Column(MutableDict.as_mutable(JSONB), nullable=True)
    hostel_details = Column(MutableDict.as_mutable(JSONB), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    # Relationships with outpass
    outpasses = relationship(
        "Outpass",
        back_populates="student",
        uselist=True,
        foreign_keys=[Outpass.student_id],
    )
    # Relationships with guardian
    guardians = relationship(
        "Guardian", back_populates="student", uselist=True, lazy="raise"
    )

    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.datetime.utcnow)

    __table_args__ = (
        Index("idx__auth_uuid", uuid),
        Index("idx__auth_roll_number", roll_number),
        Index("idx__auth_user_first_name", first_name),
        Index("idx__auth_user_last_name", last_name),
        Index("idx__auth_user_email", email),
    )

    @property
    def is_profile_complete(self):
        base_checks = [
            self.first_name,
            self.last_name,
            self.roll_number,
            self.phone_number,
        ]
        if self.account_type == "student":
            return all(
                base_checks
                + [
                    self.checklist,
                    self.checklist.get("personal_details")
                    and self.checklist.get("hostel_details")
                    and self.checklist.get("academic_details"),
                ],
            )

        if self.account_type == "warden":
            return all(
                base_checks
                + [
                    self.checklist
                    and self.checklist.get("personal_details")
                    and self.checklist.get("hostel_details"),
                ]
            )
