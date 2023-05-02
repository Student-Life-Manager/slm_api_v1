import logging
from typing import Type

from starlette.requests import Request
from starlette.responses import JSONResponse


class DetailedException(Exception):
    status_code = 400

    def __init__(
        self,
        code,
        debug_message,
        status_code=None,
        payload=None,
        log_level: int = logging.ERROR,
    ):
        self.code = code
        self.debug_message = debug_message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.log_level = log_level
        self.args = (debug_message,)

    def to_dict(self):
        return {
            "payload": self.payload or {},
            "code": self.code,
            "message": self.debug_message,
        }

    def __str__(self):
        return self.debug_message or str(self.to_dict())


class ErrorCodes:
    BAD_REQUEST = "400"
    UNAUTHORIZED = "401"
    FORBIDDEN = "403"
    NOT_FOUND = "404"
    CONFLICT = "409"
    SERVICE_UNAVAILABLE = "503"


class BadRequest(DetailedException):
    def __init__(self, message=False, code=False, payload={}):
        super().__init__(
            code=code or ErrorCodes.BAD_REQUEST,
            debug_message=message or "Bad Request",
            status_code=400,
            payload=payload,
        )


class Unauthorized(DetailedException):
    def __init__(self, message=False, code=False, payload={}):
        super().__init__(
            code=code or ErrorCodes.UNAUTHORIZED,
            debug_message=message or "Unauthorized",
            status_code=401,
            payload=payload,
        )


class Forbidden(DetailedException):
    def __init__(self, message=False, code=False, payload={}):
        super().__init__(
            code=code or ErrorCodes.FORBIDDEN,
            debug_message=message or "Forbidden",
            status_code=403,
            payload=payload,
        )


class NotFound(DetailedException):
    def __init__(self, message=False, code=False, payload={}):
        super().__init__(
            code=code or ErrorCodes.NOT_FOUND,
            debug_message=message or "Not Found",
            status_code=404,
            payload=payload,
        )


class Conflict(DetailedException):
    def __init__(self, message=False, code=False, payload={}):
        super().__init__(
            code=code or ErrorCodes.CONFLICT,
            debug_message=message or "Conflict",
            status_code=409,
            payload=payload,
        )


class ServiceUnavailable(DetailedException):
    def __init__(self, message=False, code=False, payload={}):
        super().__init__(
            code=code or ErrorCodes.SERVICE_UNAVAILABLE,
            debug_message=message or "Service Unavailable",
            status_code=503,
            payload=payload,
        )


async def exception_handler(request: Request, exc: Type[DetailedException]):
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())


ExceptionSet = {
    BadRequest,
    Unauthorized,
    Forbidden,
    NotFound,
    Conflict,
}
