from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel


class GenericReturn(BaseModel):
    ID: ClassVar[str] = "id"
    CREATED_AT: ClassVar[str] = "created_at"
    UPDATED_AT: ClassVar[str] = "updated_at"

    created_at: datetime
    updated_at: datetime | None = None
