import falcon 
from utils.patterns import SingletonMeta
from domain.entities import WorkCentersEntity

class WorkCenterBusinessValidationsRules(metaclass=SingletonMeta):

    def is_not_a_valid_work_center_data_to_register(self, work_center: WorkCentersEntity = WorkCentersEntity()) -> bool:
        if work_center.region == None or len(work_center.region) == 0:
            return True

        return False