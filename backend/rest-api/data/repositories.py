from domain.entities import WorkCentersEntity
from data.models import WorkCentersModel
from utils.patterns import RepositoryWithUnitOfWork
from data.data_source import DBDataSource
from sqlalchemy.sql.schema import Column
from utils.exceptions import DataLayerException
from utils.logger import Logger


class WorkCentersRepository(RepositoryWithUnitOfWork):

    def persist(self, entity: WorkCentersEntity) -> WorkCentersModel:
        model = WorkCentersModel(region=entity.region)

        dbSession = self._get_transaction_session()
        dbSession.add(model)
        
        return model

    def update(self, entity: WorkCentersEntity) -> WorkCentersModel:
        try:
            dbSession = self._get_transaction_session(expire_on_commit=True)
            table = dbSession.query(WorkCentersModel)

            model = table.filter_by(id=entity.id).first()
            model.fill_with_entity(entity)

            return model
        except Exception as ex:
            raise ex

    def get_all(self) -> list:
        return self._get_transaction_session().query(WorkCentersModel).all() 

    def find(self, primary_key=None) -> WorkCentersModel:
        model = (self._get_transaction_session()
                 .query(WorkCentersModel)
                 .filter_by(id=primary_key)
                 .first())

        if model != None:
            return model.to_entity()
        else:
            return None

    def delete(self, entity: WorkCentersEntity) -> bool:
        try:
            dbSession = self._get_transaction_session(expire_on_commit=True)
            table = dbSession.query(WorkCentersModel)
            filter_result = table.filter(WorkCentersModel.id == entity.id)

            if filter_result != None:
                filter_result.delete()
            else:
                raise DataLayerException(
                    "Model to delete was not found on data Source")

            return True
        except Exception as ex:
            raise ex

        return False
