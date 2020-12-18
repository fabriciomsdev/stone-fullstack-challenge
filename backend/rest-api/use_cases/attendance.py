from data.repositories import AttendanceRepository
from data.data_source import DBDataSource
from domain.entities import AttendanceEntity
from domain.business_rules import WorkCenterBusinessValidationsRules
from domain.business_messages import AttendanceOperationsRejectionMessages, DefaultOperationsRejectionsMessages
from utils.exceptions import UseCaseException


class AttendanceUseCases():
    _attendance_repository = None

    def __init__(self):
        self._attendance_repository = AttendanceRepository(
            db_data_source=DBDataSource())

    def create(self, attendance: AttendanceEntity = AttendanceEntity()) -> AttendanceEntity:
        if attendance.work_center == None:
            raise UseCaseException(AttendanceOperationsRejectionMessages.WORK_CENTER_IS_REQUIRED)

        if attendance.qty_of_terminals == None or attendance.qty_of_terminals == 0:
            raise UseCaseException(AttendanceOperationsRejectionMessages.QTY_OF_TERMINALS_IS_REQUIRED)

        if attendance.attendance_date == None:
            raise UseCaseException(AttendanceOperationsRejectionMessages.Attendance_DATE_IS_REQUIRED)

        try:
            model_created = self._attendance_repository.persist(attendance)
            self._attendance_repository.save_transaction()
        except Exception as ex:
            self._attendance_repository.revert_transaction()
            raise ex

        return model_created.to_entity()

    def get_all(self) -> list:
        return [model.to_entity() for model in self._attendance_repository.fetch()]

    def find(self, primary_key: int) -> AttendanceEntity:
        if primary_key == None or primary_key == 0:
            raise UseCaseException(DefaultOperationsRejectionsMessages.NEED_A_ID_TO_FIND)

        return self._attendance_repository.find(primary_key)

    def cancel_attendance(self, entity: AttendanceEntity) -> AttendanceEntity:
        entity.was_canceled = True
        return self.update(entity)

    def update(self, entity: AttendanceEntity) -> AttendanceEntity:
        try:
            model_updated = self._attendance_repository.update(entity)
            self._attendance_repository.save_transaction()
            return model_updated.to_entity()
        except Exception as ex:
            self._attendance_repository.revert_transaction()
            raise ex

    def delete(self, entity: AttendanceEntity) -> bool:
        try:
            self._attendance_repository.delete(entity)
            self._attendance_repository.save_transaction()
        except Exception as ex:
            self._attendance_repository.revert_transaction()
            raise ex
