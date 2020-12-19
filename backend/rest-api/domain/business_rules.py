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
        return work_center.calcule_qty_of_terminals_received() - work_center.calcule_qty_of_terminals_used()

    def get_days_coverage(self, qty_of_terminals_available: int = 0, average_of_attendence_per_days: int = 0):
        return int(qty_of_terminals_available / average_of_attendence_per_days)

    def get_coverage_classification(self, qty_of_terminals_available: int = 0, average_of_attendence_per_days: int = 0, days_used_to_count: int = 14) -> str:
        if qty_of_terminals_available == 0:
            return CoverageClassifications.RED

        if average_of_attendence_per_days == 0:
            return CoverageClassifications.GREEN

        days_coverage = self.get_days_coverage(qty_of_terminals_available, average_of_attendence_per_days)

        if days_coverage < 10 and days_coverage > 23:
            return CoverageClassifications.RED

        if (days_coverage >= 10 and days_coverage <= 13) or (days_coverage >= 19 and days_coverage <= 23):
            return CoverageClassifications.YELLOW

        if days_coverage >= 14 and days_coverage <= 18:
            return CoverageClassifications.GREEN
        
        return CoverageClassifications.RED

    def get_right_qty_to_cover_the_demand_by_days(self, days: int = 14, avg_of_consume_demand: int = 14, qty_of_terminals_available: int = 14):
        # (Media de Consumo * Quantidadde de dias) - Quantidade em disponível em estoque
        return (avg_of_consume_demand * days) - qty_of_terminals_available
        

