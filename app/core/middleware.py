import logging
import logging.config
from contextvars import ContextVar
from uuid import uuid4

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

CORRELATION_ID_CTX_KEY = "correlation_id"
REQUEST_ID_CTX_KEY = "request_id"

_correlation_id_ctx_var: ContextVar[str] = ContextVar(
    CORRELATION_ID_CTX_KEY, default=None
)
_request_id_ctx_var: ContextVar[str] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def get_correlation_id() -> str:
    return _correlation_id_ctx_var.get()


def get_request_id() -> str:
    return _request_id_ctx_var.get()


class RequestContextLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        correlation_id = _correlation_id_ctx_var.set(
            request.headers.get("X-Correlation-ID", str(uuid4()))
        )
        request_id = _request_id_ctx_var.set(str(uuid4()))

        try:
            response = await call_next(request)
        except:
            logging.exception("Exception raised")
            response = Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response.headers["X-Correlation-ID"] = get_correlation_id()
        response.headers["X-Request-ID"] = get_request_id()

        return response
