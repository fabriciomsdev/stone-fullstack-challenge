import falcon 
from utils.patterns import Singleton
from business.domain.entities import WorkCentersEntity
from business.domain.coverage_classification import CoverageClassifications

class WorkCenterBusinessRules(metaclass=Singleton):

    def is_not_a_valid_work_center_data_to_register(self, 
        work_center: WorkCentersEntity = WorkCentersEntity()) -> bool:
        """
            (BRO1) Um polo sempre deve ter uma região
        Args:
            work_center (WorkCentersEntity, optional): Polo. Defaults to WorkCentersEntity().

        Returns:
            bool: Se a entidade tiver uma região irá retornar verdadeiro se não falso
        """
        if work_center.region == None or len(work_center.region) == 0:
            return True

        return False

    def get_qty_of_terminals_available(self, work_center: WorkCentersEntity):
        """
            (BR02) A quantidade de terminais disponível é resultado das entregas das
            espedições menos a quantidade usada em atendimentos
        Args:
            work_center (WorkCentersEntity): Polo

        Returns:
            [type]: Quantidade recebida em espedições - Quantidade usada em atendimentos
        """
        return work_center.calcule_qty_of_terminals_received() - work_center.calcule_qty_of_terminals_used()

    def get_days_coverage(self, qty_of_terminals_available: int = 0, average_of_attendence_per_days: int = 0):
        """
            (BR03) - A quantidade disponível em estoque é o resultado entre a 
            subtração da quantidade disponível em estoque vinda das Expedições 
            menos a quantidade de atendimentos do polo
        Args:
            qty_of_terminals_available (int, optional): Quantidade de terminais disponíveis no momento. Defaults to 0.
            average_of_attendence_per_days (int, optional): Média de atendimentos por dia. Defaults to 0.

        Returns:
            [type]: qty_of_terminals_available / average_of_attendence_per_days
        """
        return int(qty_of_terminals_available / average_of_attendence_per_days)

    def get_coverage_classification(self, 
        qty_of_terminals_available: int = 0, 
        average_of_attendence_per_days: int = 0, days_used_to_count: int = 14) -> str:
        """
            (BR04) - Classificação de nível de cobertura:
            
            O nível de cobertura é determinado pela seguinte regra e classifições:
        Args:
            qty_of_terminals_available (int, optional): Quantidade de terminais disponíveis no momento. Defaults to 0.
            average_of_attendence_per_days (int, optional): Média de Atendimento. Defaults to 0.
            days_used_to_count (int, optional): Dias usados para calcular a média. Defaults to 14.

        Returns:
            str: 
            Se abaixo de 10 dias de cobertura -> VERMELHA (PERIGO)
            Se está entre 10 a 13 dias de cobertura -> AMARELA (ATENÇÃO)
            Se está entre 14 a 18 dias de cobertura -> VERDE (COBERTURA IDEAL)
            Se está entre 19 a 23 dias de cobertura -> AMARELA (ATENÇÃO)
            Se está entre acima de 23 de cobertura -> VERMELHA (PERIGO)
        """

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

    def get_right_qty_to_cover_the_demand_by_days(self, 
        days: int = 14, avg_of_consume_demand: int = 14, qty_of_terminals_available: int = 14):
        """
            (BR05) - A Predição de demanda necessária
            P = (MD * D) - QuantityOfTerminalsAvailable
        Args:
            days (int, optional):  Dias usados para calcular a média diara de consumo. Defaults to 14.
            avg_of_consume_demand (int, optional): Média diária de consumo. Defaults to 14.
            qty_of_terminals_available (int, optional): Quantidade de terminais disponíveis no momento. Defaults to 14.

        Returns:
            int: prediction of terminals needly
        """
        return (avg_of_consume_demand * days) - qty_of_terminals_available
        

