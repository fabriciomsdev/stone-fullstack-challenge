from data.repositories import WorkCentersRepository
from data.data_source import DBDataSource
from data.models import WorkCentersModel
from business.domain.entities import WorkCentersEntity
from business.rules import WorkCenterBusinessRules
from business.messages import (
    WorkCenterOperationsRejectionMessages, 
    DefaultOperationsRejectionsMessages
)
from utils.exceptions import UseCaseException


class WorkCentersUseCases():
    _work_centers_repository: WorkCentersRepository = None
    _business_rules: WorkCenterBusinessRules = None
    _data_source = None

    def __init__(self, data_source: DBDataSource):
        self._data_source = data_source
        self._work_centers_repository = WorkCentersRepository(
            db_data_source=self._data_source)
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


    def update_calculated_values(self, entity: WorkCentersEntity) -> WorkCentersEntity:
        if entity is not None:
            entity_updated = self._work_centers_repository.find(entity.id)

            entity_updated.days_qty_ideal_for_coverage = 14
            entity_updated.calcule_qty_of_terminals_used()
            entity_updated.calcule_qty_of_terminals_received()
            entity_updated.calcule_qty_of_terminals_available()
            
            entity_updated.avg_of_attendence = self.get_average_of_attendences_in_wc(
                entity_updated, entity_updated.days_qty_ideal_for_coverage)
            
            entity_updated.days_of_coverage = self._business_rules.get_days_coverage(
                entity_updated.qty_of_terminals_available,
                entity_updated.avg_of_attendence
            )

            entity_updated.coverage_classification = self._business_rules.get_coverage_classification(
                entity_updated.qty_of_terminals_available, 
                entity_updated.avg_of_attendence, 
                entity_updated.days_qty_ideal_for_coverage)
            
            model = self._work_centers_repository.update(entity_updated)
            
            self._work_centers_repository.save_transaction()
            self._work_centers_repository.refresh_data(model)

            return model.to_entity()
        
        return entity


    def get_all(self) -> list:
        work_centers_list = []
        work_centers_in_DS = self._work_centers_repository.fetch()

        for model in work_centers_in_DS:
            self._work_centers_repository.refresh_data(model)
            model.to_entity()
            work_centers_list.append(model)

        return work_centers_list 


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
