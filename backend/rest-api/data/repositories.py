from domain.entities import WorkCentersEntity
from data.models import AbstractModel, WorkCentersModel
from data.data_source import DBDataSource
from sqlalchemy.sql.schema import Column
from utils.logger import Logger
from data.abstract import AbstractRepositoryWithUnitOfWork

class WorkCentersRepository(AbstractRepositoryWithUnitOfWork[WorkCentersEntity, WorkCentersModel]):
    def _get_model_class(self) -> WorkCentersModel:
        return WorkCentersModel


