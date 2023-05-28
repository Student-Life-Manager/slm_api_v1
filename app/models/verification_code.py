from sqlalchemy import BigInteger, Column, DateTime, String
from sqlalchemy.sql.functions import func

from app.database.setup import Base


class VerificationCode(Base):
    __tablename__ = "verification_code"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    phone_number = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True)

    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )