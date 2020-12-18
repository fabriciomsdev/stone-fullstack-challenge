from domain.entities import WorkCentersEntity, ExpeditionsEntity, AttendanceEntity
from data.models import AbstractModel, WorkCentersModel, ExpeditionsModel, AttendanceModel
from data.data_source import DBDataSource
from sqlalchemy.sql.schema import Column
from utils.logger import Logger
from data.abstract import AbstractRepositoryWithUnitOfWork

class WorkCentersRepository(AbstractRepositoryWithUnitOfWork[WorkCentersEntity, WorkCentersModel]):
    def _get_model_class(self) -> WorkCentersModel:
        return WorkCentersModel


class ExpeditionsRepository(AbstractRepositoryWithUnitOfWork[ExpeditionsEntity, ExpeditionsModel]):
    def _get_model_class(self) -> ExpeditionsModel:
        return ExpeditionsModel


class AttendanceRepository(AbstractRepositoryWithUnitOfWork[AttendanceEntity, AttendanceModel]):
    def _get_model_class(self) -> AttendanceModel:
        return AttendanceModel




