from datetime import datetime, timezone
from functools import reduce
from typing import Any, Dict, Generic, List, Type, TypeVar
from uuid import UUID

from sqlalchemy.orm import Query, Session

from app.database.setup import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model_class: Type[ModelType] = model

    def new(self, attributes: dict[str, Any]) -> ModelType:
        model = self.model_class(**attributes)
        self.db.add(model)

        return model

    def create(self, attributes: dict[str, Any]) -> ModelType:
        # attributes["created_at"] = datetime.now(timezone.utc)
        model = self.model_class(**attributes)

        self.db.add(model)
        self.db.commit()

        return model

    def multi_create(self, attributes_list: list[dict[str, Any]]) -> list[ModelType]:
        models = [
            self.model_class(**attributes, created_at=datetime.now(timezone.utc))
            for attributes in attributes_list
        ]
        self.db.add_all(models)
        self.db.commit()

        return models

    def update(self, model: ModelType, attributes: dict[str, Any]) -> ModelType:
        attributes["updated_at"] = datetime.now(timezone.utc)

        for field in attributes:
            setattr(model, field, attributes[field])

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return model

    def multi_update(
        self, models: list[ModelType], attributes_list: list[dict[str, Any]]
    ) -> list[ModelType]:
        updated_models = []
        for model, attributes in zip(models, attributes_list):
            attributes["updated_at"] = datetime.now(timezone.utc)

            for field in attributes:
                setattr(model, field, attributes[field])

            updated_models.append(model)

        self.db.add_all(updated_models)
        self.db.commit()

        for updated_model in updated_models:
            self.db.refresh(updated_model)

        return updated_models

    def insert(self, model: ModelType) -> ModelType:
        model.created_at = datetime.now(timezone.utc)

        self.db.add(model)
        self.db.commit()

        return model

    def save(self):
        self.db.commit()

    def delete(self, model: ModelType) -> bool:
        self.db.delete(model)
        self.db.commit()
        self.db.expire_all()
        return True

    def get(self, id_: int, with_: list | None = None) -> ModelType | None:
        query = self._queryable(with_)
        query = self._by_id(query, id_)

        return query.first()

    def get_by_id(self, id: int, with_: list | None = None) -> ModelType | None:
        query = self._queryable(with_)
        query = self._by_id(query, id)

        return query.first()

    def get_by_uuid(self, uuid: UUID, with_: list | None = None) -> ModelType | None:
        query = self._queryable(with_)
        query = self._by_uuid(query, uuid)

        return query.first()

    def get_bulk_by_uuid(
        self, uuids: List[UUID], with_: list | None = None
    ) -> List[ModelType] | None:
        return self._queryable(with_).filter(self.model_class.uuid.in_(uuids)).all()

    def get_multi(
        self, skip: int = 0, limit: int = 100, with_: list | None = None
    ) -> list[ModelType]:
        query = self._queryable(with_)
        query = query.offset(skip).limit(limit)

        return query.all()

    def lock_for_update(self, model: ModelType):
        (
            self.db.query(self.model_class)
            .filter(self.model_class.uuid == model.uuid)
            .with_for_update()
        )

    def _queryable(self, with_: list | None) -> Query:
        query = self.db.query(self.model_class)
        query = self._maybe_with(query, with_)

        return query

    def _by_id(self, query: Query, id_: int) -> Query:
        return query.filter(self.model_class.id == id_)

    def _by_uuid(
        self,
        query: Query,
        uuid: UUID,
    ) -> Query:
        return query.filter(self.model_class.uuid == uuid)

    def _maybe_with(self, query: Query, with_: list | None = None):
        if with_:
            return reduce(self._add_join_to_query, with_, query)

        return query

    def _add_join_to_query(self, query, with_):
        return getattr(self, "_with_" + with_)(query)
