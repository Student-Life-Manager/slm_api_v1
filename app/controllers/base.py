from typing import Any, Generic, Set, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.exceptions import NotFound
from app.crud import CRUDBase
from app.database.setup import Base

ModelType = TypeVar("ModelType", bound=Base)
UpdateType = TypeVar("UpdateType", bound=BaseModel)


class BaseController(Generic[ModelType, UpdateType]):
    def __init__(self, db: Session, model: Type[ModelType], crud_instance: CRUDBase):
        self.db = db
        self.model_class = model
        self.crud_instance = crud_instance

    def update_jsonb_attr(
        self, db_obj: ModelType, attributes: dict[str, Any], attribute_name: str
    ) -> str:
        value_db = db_obj.__dict__[attribute_name]
        value = attributes[attribute_name]

        for key in value:
            value_db[key] = value[key]

        return value_db

    def get(self, id_: int, with_: list | None = None) -> ModelType:
        db_obj = self.crud_instance.get(id_, with_)
        if not db_obj:
            raise NotFound(
                f"{self.model_class.__tablename__.title()} with id: {id_} does not exist"
            )

        return db_obj

    def get_by_uuid(self, uuid: UUID, with_: list | None = None) -> ModelType:
        db_obj = self.crud_instance.get_by_uuid(uuid, with_)
        if not db_obj:
            raise NotFound(
                f"{self.model_class.__tablename__.title()} with uuid: {uuid} does not exist"
            )
        return db_obj

    def get_multi(
        self, skip: int = 0, limit: int = 100, with_: list | None = None
    ) -> list[ModelType]:
        return self.crud_instance.get_multi(skip, limit, with_)

    @staticmethod
    def extract_attributes_from_schema(
        schema: BaseModel, excludes: Set = None
    ) -> dict[str, Any]:
        return schema.dict(exclude=excludes, exclude_unset=True)

    def update(self, db_obj: ModelType, update_obj: UpdateType) -> ModelType:
        attributes = BaseController.extract_attributes_from_schema(update_obj)
        return self.crud_instance.update(db_obj, attributes)

    def delete(self, model: ModelType) -> bool:
        return self.crud_instance.delete(model)
