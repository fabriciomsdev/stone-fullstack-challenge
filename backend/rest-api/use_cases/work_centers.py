from data.repositories import WorkCentersRepository
from data.data_source import DBDataSource
from domain.entities import WorkCentersEntity
from domain.business_rules import WorkCenterBusinessRules
from domain.business_messages import WorkCenterOperationsRejectionMessages, DefaultOperationsRejectionsMessages
from utils.exceptions import UseCaseException


class WorkCentersUseCases():
    _work_centers_repository: WorkCentersRepository = None
    _business_rules: WorkCenterBusinessRules = None

    def __init__(self):
        self._work_centers_repository = WorkCentersRepository(db_data_source = DBDataSource())
        self._business_rules = WorkCenterBusinessRules()   

    def get_average_of_attendences_in_wc(self, work_center: WorkCentersEntity = WorkCentersEntity(), days: int = 14) -> int:
        return self._work_centers_repository.get_average_of_attendence_by_days_period(work_center, 14)

    def create(self, work_center: WorkCentersEntity = WorkCentersEntity()) -> WorkCentersEntity:
        if work_center == {}:
            raise UseCaseException(
                WorkCenterOperationsRejectionMessages.INVALID_REGION_NAME)

        if self._business_rules.is_not_a_valid_work_center_data_to_register(work_center):
            raise UseCaseException(
                WorkCenterOperationsRejectionMessages.INVALID_DATA_TO_REGISTER)

        try:
            model_created = self._work_centers_repository.persist(work_center)
            self._work_centers_repository.save_transaction()
        except Exception as ex:
            self._work_centers_repository.revert_transaction()
            raise ex

        return model_created.to_entity()

    def get_all(self) -> list:
        return [ model.to_entity() for model in self._work_centers_repository.fetch() ]

    def find(self, primary_key: int) -> WorkCentersEntity:
        if primary_key == None or primary_key == 0:
            raise UseCaseException(
                DefaultOperationsRejectionsMessages.NEED_A_ID_TO_FIND)

        return self._work_centers_repository.find(primary_key)

    def delete(self, entity: WorkCentersEntity) -> bool:
        try:
            self._work_centers_repository.delete(entity)
            self._work_centers_repository.save_transaction()
        except Exception as ex:
            self._work_centers_repository.revert_transaction()
            raise ex

    def update(self, entity: WorkCentersEntity) -> WorkCentersEntity:
        try:
            model_updated = self._work_centers_repository.update(entity)
            self._work_centers_repository.save_transaction()
            return model_updated.to_entity()
        except Exception as ex:
            self._work_centers_repository.revert_transaction()
            raise ex
