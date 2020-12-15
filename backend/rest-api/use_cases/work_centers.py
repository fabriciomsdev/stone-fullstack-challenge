from data.repositories import WorkCentersRepository
from domain.entities import WorkCentersEntity
from domain.business_rules import WorkCenterBusinessValidationsRules
from domain.business_messages import WorkCenterOperationsRejectionMessages

class WorkCentersUseCases():

    def create(self, work_center: WorkCentersEntity = WorkCentersEntity()) -> WorkCentersEntity:
        if work_center == {}:
            raise Exception(WorkCenterOperationsRejectionMessages.INVALID_REGION_NAME)

        if WorkCenterBusinessValidationsRules().is_not_a_valid_work_center_data_to_register(work_center):
            raise Exception(WorkCenterOperationsRejectionMessages.INVALID_DATA_TO_REGISTER)
        
        return WorkCentersRepository().persist(work_center)

    def get_all(self) -> list:
        return WorkCentersRepository().get_all()




        



        
