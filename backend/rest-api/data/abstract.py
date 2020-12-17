from typing import TypeVar, Generic
from data.orm import BaseModel
from utils.patterns import RepositoryWithUnitOfWork
from utils.exceptions import DataLayerException
from sqlalchemy import Column, String, Integer, ForeignKey

entityType = TypeVar('entityType')

class AbstractModel(Generic[entityType]):
    id = Column(Integer, primary_key=True)

    def fill_with_entity(self, entity: entityType = None):
        pass

    def to_entity(self) -> entityType:
        return entityType


modelType = TypeVar('AbstractModel', AbstractModel, bytes)


class AbstractRepositoryWithUnitOfWork(Generic[entityType, modelType], RepositoryWithUnitOfWork):

    def _get_model_class(self) -> AbstractModel:
        return AbstractModel

    def fill_model(self, entity: entityType) -> modelType:
        model = self._get_model_class()()
        model.fill_with_entity(entity)
        return model

    def persist(self, entity: entityType) -> modelType:
        model = self.fill_model(entity)

        dbSession = self._get_transaction_session()
        dbSession.add(model)

        return model

    def update(self, entity: entityType) -> modelType:
        try:
            dbSession = self._get_transaction_session(expire_on_commit=True)
            table = dbSession.query(self._get_model_class())

            model = table.filter_by(id=entity.id).first()
            model.fill_with_entity(entity)

            return model
        except Exception as ex:
            raise ex

    def fetch(self) -> list:
        return self._get_transaction_session().query(self._get_model_class()).all()

    def find(self, primary_key=None) -> modelType:
        model = (self._get_transaction_session()
                 .query(self._get_model_class())
                 .filter_by(id=primary_key)
                 .first())

        if model != None:
            return model.to_entity()
        else:
            return None

    def delete(self, entity: entityType) -> bool:
        try:
            model_class = self._get_model_class()
            dbSession = self._get_transaction_session(expire_on_commit=True)
            table = dbSession.query(model_class)
            filter_result = table.filter(model_class.id == entity.id)

            if filter_result != None:
                filter_result.delete()
            else:
                raise DataLayerException(
                    "Model to delete was not found on data Source")

            return True
        except Exception as ex:
            raise ex

        return False
