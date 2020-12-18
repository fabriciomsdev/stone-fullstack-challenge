from domain.entities import WorkCentersEntity, ExpeditionsEntity
from data.orm import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from typing import TypeVar, Generic
from data.abstract import AbstractModel
from sqlalchemy.types import Boolean
from sqlalchemy.orm import relationship

models_tables = {
    'WorkCentersModel': 'work_centers',
    'ExpeditionsModel': 'expeditions'
}

class WorkCentersModel(AbstractModel[WorkCentersEntity], BaseModel, WorkCentersEntity):
    __tablename__ = models_tables['WorkCentersModel']
    region = Column(String)
    expeditions = relationship(
        "ExpeditionsModel", back_populates="work_center", post_update=False)

    def fill_with_entity(self, entity: WorkCentersEntity = None):
        self.id = entity.id
        self.region = entity.region

    def to_entity(self) -> WorkCentersEntity:
        expeditions = [ exp.to_entity() for exp in self.expeditions ]
        return WorkCentersEntity(self.region, self.id, self.expeditions)


class ExpeditionsModel(AbstractModel[WorkCentersEntity], BaseModel, ExpeditionsEntity):
    __tablename__ = models_tables['ExpeditionsModel']
    qty_of_items = Column(Integer)
    was_canceled = Column(Boolean)
    work_center_id = Column(Integer, ForeignKey('{work_centers_table}.id'.format(
        work_centers_table = models_tables['WorkCentersModel'])))
    work_center = relationship(
        "WorkCentersModel", back_populates="expeditions", post_update=False)

    def fill_with_entity(self, entity: ExpeditionsEntity):
        self.id = entity.id
        self.qty_of_items = entity.qty_of_items
        self.was_canceled = entity.was_canceled
        self.work_center_id = entity.work_center.id

    def to_entity(self) -> ExpeditionsEntity:
        return ExpeditionsEntity(self.id, self.qty_of_items, self.was_canceled, self.work_center)
