import falcon 
from utils.patterns import Singleton
from domain.entities import WorkCentersEntity
from domain.coverage_classification import CoverageClassifications

class WorkCenterBusinessRules(metaclass=Singleton):

    def is_not_a_valid_work_center_data_to_register(self, work_center: WorkCentersEntity = WorkCentersEntity()) -> bool:
        if work_center.region == None or len(work_center.region) == 0:
            return True

        return False

    def get_qty_of_terminals_available(self, work_center: WorkCentersEntity):
        return work_center.get_qty_of_terminals_received() - work_center.get_qty_of_terminals_used()

    def get_days_coverage(self, qty_of_terminals_available: int = 0, average_of_attendence_per_days: int = 0):
        return int(qty_of_terminals_available / average_of_attendence_per_days)

    def get_coverage_classification(self, qty_of_terminals_available: int = 0, average_of_attendence_per_days: int = 0, days_used_to_count: int = 14) -> str:
        classification = CoverageClassifications.RED

        if qty_of_terminals_available == 0:
            classification = CoverageClassifications.RED

        if average_of_attendence_per_days == 0:
            classification = CoverageClassifications.GREEN

        days_coverage = self.get_days_coverage(qty_of_terminals_available, average_of_attendence_per_days)

        if days_coverage < 10 and days_coverage > 23:
            classification = CoverageClassifications.RED

        if (days_coverage >= 10 and days_coverage <= 13) or (days_coverage >= 19 and days_coverage <= 23):
            classification = CoverageClassifications.YELLOW

        if days_coverage >= 14 and days_coverage <= 18:
            classification = CoverageClassifications.GREEN

        return classification
        

