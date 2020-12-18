from utils.json import ComplexObjectToJsonEntityMixin
from datetime import datetime

class WorkCentersEntity(ComplexObjectToJsonEntityMixin):
    id: int = None
    region: str = ''
    expeditions: list = []
    attendance: list = []

    def __init__(self, region: str = None, id: int = None, expeditions: list = [], attendance: list = []):
        self.id = id
        self.fill(region, expeditions, attendance)

    def fill(self, region: str = None, expeditions: list = [], attendance: list = []):
        self.region = region
        self.expeditions = expeditions
        self.attendance = attendance

    def get_qty_of_terminals_received(self):
        terminals_delivered_list = [ 
            exp.qty_of_terminals for exp in self.expeditions if exp.was_canceled == False
        ]

        return sum(terminals_delivered_list)

    def get_qty_of_terminals_used(self):
        terminals_delivered_list = [
            attdc.qty_of_terminals for attdc in self.attendance if attdc.was_canceled == False
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

