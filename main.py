from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from app.api.endpoints.api import router
from app.core.config import settings
from app.core.exceptions import ExceptionSet, exception_handler
from app.core.logging import setup_requests_logging, setup_sql_logging

app = FastAPI(title="slm", version=1)
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if exception_handler:
    for exception in ExceptionSet:
        app.add_exception_handler(exception, exception_handler)


if settings.SHOW_SQL_ALCHEMY_QUERIES:
    setup_sql_logging()

if settings.SHOW_OUTGOING_REQUESTS:
    setup_requests_logging(),
