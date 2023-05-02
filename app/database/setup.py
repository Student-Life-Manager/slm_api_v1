from typing import Any

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr


# this is a base model
@as_declarative()
class Base:
    id: Any  # id can be str too,
    uuid: UUID
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
