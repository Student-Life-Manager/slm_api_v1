from datetime import datetime, timedelta

from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings
from app.core.exceptions import Unauthorized

ALGORITHM = settings.AUTH_CONFIG.JWT_ALGORITHM
SECRET_KEY = settings.AUTH_CONFIG.JWT_SECRET_KEY


class JWTHandler:
    @staticmethod
    def encode(payload: dict, days: int = 1) -> str:
        expire = datetime.utcnow() + timedelta(days=days)
        payload.update({"exp": expire})
        return jwt.encode(payload, SECRET_KEY, ALGORITHM)

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except ExpiredSignatureError as exception:
            raise Unauthorized(message="Token expired.")
        except JWTError as exception:
            print(exception, flush=True)

    @staticmethod
    def decode_expire(token: str) -> dict:
        try:
            return jwt.decode(
                token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False}
            )
        except JWTError as exception:
            print(exception, flush=True)


# - go to this doc, do this
