from utils.json import ComplexObjectToJsonEntityMixin

class WorkCentersEntity(ComplexObjectToJsonEntityMixin):
    id: int = None
    region: str = ''
    expeditions: list

    def __init__(self, region: str = None, id: int = None, expeditions: list = []):
        self.id = id
        self.fill(region, expeditions)

    def fill(self, region: str = None, expeditions: list = []):
        self.region = region
        self.expeditions = expeditions

    def qty_of_terminals_on_stock(self):
        expeditions = self.expeditions
        terminals_delivered_list = [ 
            exp.qty_of_terminals for exp in expeditions if exp.was_canceled == False
        ]

        return sum(terminals_delivered_list)


class ExpeditionsEntity(ComplexObjectToJsonEntityMixin):
    id: int = None
    qty_of_terminals: int = 1
    was_canceled: bool = False
    work_center: WorkCentersEntity = None

    def __init__(self, id: int = None, qty_of_terminals: int = 1, was_canceled: bool = False, work_center: WorkCentersEntity = None):
        self.id = id
        self.fill(qty_of_terminals, was_canceled, work_center)

    def fill(self, qty_of_terminals: str = None, was_canceled: bool = False, work_center: WorkCentersEntity = None):
        self.qty_of_terminals = qty_of_terminals
        self.was_canceled = was_canceled
        
        if work_center != None:
            self.work_center = work_center

