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
    guardian_1_name = Column(String)
    guardian_1_phone_number = Column(String)
    guardian_2_name = Column(String)
    guardian_2_phone_number = Column(String)


    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.datetime.utcnow)

    __table_args__ = (
        Index("idx__auth_uuid", uuid),
        Index("idx__auth_roll_number", roll_number),
        Index("idx__auth_user_email", email),
    )
