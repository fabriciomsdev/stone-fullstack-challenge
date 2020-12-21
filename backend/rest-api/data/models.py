from business.domain.entities import (
    WorkCentersEntity, 
    ExpeditionsEntity, 
    AttendanceEntity
)
from data.orm import BaseModel
from sqlalchemy import (
    Column, 
    String, 
    Integer, 
    ForeignKey, 
    DateTime
)
from typing import TypeVar, Generic
from data.abstract import AbstractModel
from sqlalchemy.types import Boolean
from sqlalchemy.orm import relationship
from enum import Enum

models_tables = {
    'WorkCentersModel': 'work_centers',
    'ExpeditionsModel': 'expeditions',
    'AttendanceModel': 'attendance'
}

class WorkCentersModel(AbstractModel[WorkCentersEntity], BaseModel, WorkCentersEntity):
    __tablename__ = models_tables['WorkCentersModel']
    region = Column(String(256))
    days_qty_ideal_for_coverage = Column(Integer)
    coverage_classification = Column(String(256))
    days_of_coverage = Column(Integer)
    avg_of_attendence = Column(Integer)
    qty_of_terminals_available = Column(Integer)
    qty_of_terminals_used = Column(Integer)
    qty_of_terminals_received = Column(Integer)

    expeditions = relationship(
        "ExpeditionsModel", 
        back_populates="work_center", 
        post_update=True, 
        cascade="all")
    attendance = relationship(
        "AttendanceModel", 
        back_populates="work_center", 
        post_update=True)

    def fill_with_entity(self, entity: WorkCentersEntity = None):
        self.id = entity.id
        self.region = entity.region
        self.days_qty_ideal_for_coverage = entity.days_qty_ideal_for_coverage
        self.days_of_coverage = entity.days_of_coverage
        self.avg_of_attendence = entity.avg_of_attendence
        self.qty_of_terminals_available = entity.qty_of_terminals_available
        self.qty_of_terminals_used = entity.qty_of_terminals_used
        self.qty_of_terminals_received = entity.qty_of_terminals_received

        if (isinstance(entity.coverage_classification, str) 
            and not isinstance(entity.coverage_classification, Enum)):
            self.coverage_classification= entity.coverage_classification
            
        elif isinstance(entity.coverage_classification, str):
            self.coverage_classification = entity.coverage_classification.value
        

    def to_entity(self) -> WorkCentersEntity:
        expeditions = [ exp.to_entity() for exp in self.expeditions ]
        attendance = [ attdc.to_entity() for attdc in self.attendance ]

        return WorkCentersEntity(
            self.region, 
            self.id, 
            expeditions, 
            attendance, 
            self.days_qty_ideal_for_coverage,
            self.coverage_classification,
            self.days_of_coverage,
            self.avg_of_attendence,
            self.qty_of_terminals_available,
            self.qty_of_terminals_used,
            self.qty_of_terminals_received)


class ExpeditionsModel(AbstractModel[WorkCentersEntity], BaseModel, ExpeditionsEntity):
    __tablename__ = models_tables['ExpeditionsModel']
    qty_of_terminals = Column(Integer)
    was_canceled = Column(Boolean)
    work_center_id = Column(Integer, ForeignKey('{work_centers_table}.id'.format(
        work_centers_table = models_tables['WorkCentersModel'])))
    work_center = relationship(
        "WorkCentersModel", 
        back_populates="expeditions", 
        post_update=True)
    auto_predict_qty_needed = Column(Boolean)
    
    
    def fill_with_entity(self, entity: ExpeditionsEntity):
        self.id = entity.id
        self.qty_of_terminals = entity.qty_of_terminals
        self.was_canceled = entity.was_canceled
        self.work_center_id = entity.work_center.id
        self.auto_predict_qty_needed = entity.auto_predict_qty_needed

    def to_entity(self) -> ExpeditionsEntity:
        return ExpeditionsEntity(
            self.id, 
            self.qty_of_terminals, 
            self.was_canceled, 
            self.work_center, 
            self.auto_predict_qty_needed
        )


class AttendanceModel(AbstractModel[WorkCentersEntity], BaseModel, AttendanceEntity):
    __tablename__ = models_tables['AttendanceModel']
    qty_of_terminals = Column(Integer)
    was_canceled = Column(Boolean)
    work_center_id = Column(Integer, ForeignKey('{work_centers_table}.id'.format(
        work_centers_table=models_tables['WorkCentersModel'])))
    work_center = relationship(
        "WorkCentersModel", 
        back_populates="attendance", 
        post_update=True)


    def fill_with_entity(self, entity: AttendanceEntity):
        self.id = entity.id
        self.qty_of_terminals = entity.qty_of_terminals
        self.was_canceled = entity.was_canceled
        self.work_center_id = entity.work_center.id
        self.attendance_date = entity.attendance_date

    def to_entity(self) -> AttendanceEntity:
        return AttendanceEntity(
            self.id, 
            self.qty_of_terminals, 
            self.was_canceled, 
            self.work_center, 
            self.attendance_date
        )
