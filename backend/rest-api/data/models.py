from domain.entities import WorkCentersEntity
from data.orm import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from typing import TypeVar, Generic
from data.abstract import AbstractModel

class WorkCentersModel(AbstractModel[WorkCentersEntity], BaseModel, WorkCentersEntity):
    __tablename__ = 'work_centers'
    region = Column(String)

    def fill_with_entity(self, entity: WorkCentersEntity = None):
        if entity != None:
            self.id = entity.id
            self.region = entity.region

    def to_entity(self) -> WorkCentersEntity:
        return WorkCentersEntity(self.region, self.id)
