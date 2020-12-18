from utils.json import ComplexObjectToJsonEntityMixin
from datetime import datetime

class WorkCentersEntity(ComplexObjectToJsonEntityMixin):
    id: int = None
    region: str = ''
    expeditions: list = []
    attendance: list = []
    coverage_classification: str = None
    days_of_coverage: int = 0
    avg_of_attendence: int = 0
    coverage_based_on_days_qty: int = 14
    qty_of_terminals_available: int = 0
    qty_of_terminals_used: int = 0
    qty_of_terminals_received: int = 0

    def __init__(self, region: str = None, id: int = None, expeditions: list = [], attendance: list = []):
        self.id = id
        self.fill(region, expeditions, attendance)

    def fill(self, region: str = None, expeditions: list = [], attendance: list = []):
        self.region = region
        self.expeditions = expeditions
        self.attendance = attendance

    def calcule_qty_of_terminals_received(self) -> int:
        terminals_delivered_list = [ 
            exp.qty_of_terminals for exp in self.expeditions if exp.was_canceled == False
        ]
        self.qty_of_terminals_received = sum(terminals_delivered_list)

        return self.qty_of_terminals_received

    def calcule_qty_of_terminals_used(self) -> int:
        terminals_delivered_list = [
            attdc.qty_of_terminals for attdc in self.attendance if attdc.was_canceled == False
        ]
        self.qty_of_terminals_used = sum(terminals_delivered_list)

        return self.qty_of_terminals_used

    def calcule_qty_of_terminals_available(self) -> int:
        if self.qty_of_terminals_used == 0:
            self.calcule_qty_of_terminals_used()

        if self.qty_of_terminals_received == 0:
            self.calcule_qty_of_terminals_received()

        self.qty_of_terminals_available = self.qty_of_terminals_received - self.qty_of_terminals_used

        return self.qty_of_terminals_available


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


class AttendanceEntity(ComplexObjectToJsonEntityMixin):
    id: int = None
    qty_of_terminals: int = 1
    was_canceled: bool = False
    work_center: WorkCentersEntity = None
    attendance_date: datetime = datetime.now()

    def __init__(self, id: int = None, qty_of_terminals: int = 1, was_canceled: bool = False, work_center: WorkCentersEntity = None, attendance_date: datetime = None):
        self.id = id
        self.fill(qty_of_terminals, was_canceled, work_center, attendance_date)

    def fill(self, qty_of_terminals: str = None, was_canceled: bool = False, work_center: WorkCentersEntity = None, attendance_date: datetime = None):
        self.qty_of_terminals = qty_of_terminals
        self.was_canceled = was_canceled

        if work_center != None:
            self.work_center = work_center

        if attendance_date != None:
            self.attendance_date = attendance_date

