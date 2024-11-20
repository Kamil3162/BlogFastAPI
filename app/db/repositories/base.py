import typing

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session
from pydantic import BaseModel
import sqlalchemy


ModelType = typing.TypeVar("ModelType", bound=DeclarativeMeta)

class BaseRepository:
    def __init__(self, model: typing.TypeVar[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: int):
        '''
        Retrieve a record by its ID.

        Args:
            id: Primary key value

        Returns:
            Optional[ModelType]: Found record or None
        '''

        query = sqlalchemy.select(self.model).where(self.model.id == id)
        result = self.db.query(query)
        return result

    def get_by_attribute(
            self,
            attr_name: str,
            attr_value: typing.Any
    ) -> typing.Optional[ModelType]:
        '''
            Retrieve a record by a specific attribute.

            Args:
                attr_name: Name of the attribute/column
                attr_value: Value to search for

            Return:

        '''
        query = (sqlalchemy.select(self.model).
            where(getattr(self.model, attr_name) == attr_value))
        result = self.db.query(query)
        return result

    def create(
        self,
        schema: BaseModel
    ) -> typing.Optional[BaseModel]:
        '''


        '''
        db_object = self.model(**schema)
        self.db.add(db_object)
        self.db.commit()
        self.db.refresh(db_object)
        return db_object


    def update(
        self,
        db_obj: ModelType,
        schema: BaseModel
    ) -> typing.Optional[BaseModel]:
        _obj_data = db_obj.metadata.schema

        for field in _obj_data:
            if field in schema:
                setattr(_obj_data, field, schema[field])

        self.db.add(_obj_data)
        self.db.commit()
        self.db.refresh(_obj_data)
        return _obj_data

    def delete(self, id: int) -> bool:
        query = sqlalchemy.delete(self.model).where(self.model.id == id)
        result = self.db.execute(query)
        self.db.commit()
        return result.rowcount > 0
