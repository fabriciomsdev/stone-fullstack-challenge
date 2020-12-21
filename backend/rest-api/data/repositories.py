import datetime
from data.data_source import DBDataSource
from sqlalchemy.sql.schema import Column
from sqlalchemy import desc
from utils.logger import Logger
from data.abstract import AbstractRepositoryWithUnitOfWork

from business.domain.entities import (
    WorkCentersEntity, 
    ExpeditionsEntity, 
    AttendanceEntity
)
from data.models import (
    AbstractModel, 
    WorkCentersModel, 
    ExpeditionsModel, 
    AttendanceModel
)



class WorkCentersRepository(AbstractRepositoryWithUnitOfWork[WorkCentersEntity, WorkCentersModel]):
    def _get_model_class(self) -> WorkCentersModel:
        return WorkCentersModel

    def get_average_of_attendence_by_days_period(self, wc: WorkCentersEntity, days_period: int = 14) -> int:
        base_date = datetime.datetime.today()
        days_to_discount = datetime.timedelta(days_period)
        dbSession = self._get_transaction_session()

        last_attendance = dbSession.query(AttendanceModel).filter(
            AttendanceModel.work_center_id == wc.id,
            AttendanceModel.was_canceled == False
        ).order_by(desc(AttendanceModel.id)).first()

        if last_attendance is not None:
            base_date = last_attendance.attendance_date

        first_day_to_count = base_date - days_to_discount

        dbSession = self._get_transaction_session()
        attendences_in_period = dbSession.query(AttendanceModel).filter(
            AttendanceModel.attendance_date >= first_day_to_count,
            AttendanceModel.attendance_date <= base_date,
            AttendanceModel.work_center_id == wc.id,
            AttendanceModel.was_canceled == False).all()
        
        terminals_used = [ attdc.qty_of_terminals for attdc in attendences_in_period ]
        terminals_used_qty = sum(terminals_used)
        
        if terminals_used_qty != 0 and days_period != 0:
            if terminals_used_qty > days_period:
                return int(terminals_used_qty / days_period)
            else:
                return terminals_used_qty

        return 0


class ExpeditionsRepository(AbstractRepositoryWithUnitOfWork[ExpeditionsEntity, ExpeditionsModel]):
    def _get_model_class(self) -> ExpeditionsModel:
        return ExpeditionsModel


class AttendanceRepository(AbstractRepositoryWithUnitOfWork[AttendanceEntity, AttendanceModel]):
    def _get_model_class(self) -> AttendanceModel:
        return AttendanceModel






