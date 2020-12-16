from data.repositories import WorkCentersRepository
from domain.entities import WorkCentersEntity
from domain.business_rules import WorkCenterBusinessValidationsRules
from domain.business_messages import WorkCenterOperationsRejectionMessages
from utils.exceptions import UseCaseException

class WorkCentersUseCases():
    _work_centers_repository = WorkCentersRepository()

    def create(self, work_center: WorkCentersEntity = WorkCentersEntity()) -> WorkCentersEntity:
        if work_center == {}:
            raise UseCaseException(WorkCenterOperationsRejectionMessages.INVALID_REGION_NAME)

        if WorkCenterBusinessValidationsRules().is_not_a_valid_work_center_data_to_register(work_center):
            raise UseCaseException(WorkCenterOperationsRejectionMessages.INVALID_DATA_TO_REGISTER)

        try:
            entity_created = self._work_centers_repository.persist(work_center)
            self._work_centers_repository.save_transaction()
        except Exception as ex:
            self._work_centers_repository.revert_transaction()
            raise ex

        return entity_created

    def get_all(self) -> list:
        return self._work_centers_repository.get_all()

    def find(self, primary_key: int) -> WorkCentersEntity:
        if primary_key == None or primary_key == 0:
            raise UseCaseException(WorkCenterOperationsRejectionMessages.NEED_A_ID_TO_FIND)
        
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
            self._work_centers_repository.update(entity)
            self._work_centers_repository.save_transaction()
        except Exception as ex:
            self._work_centers_repository.revert_transaction()
            raise ex





        



        
