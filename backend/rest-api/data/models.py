from domain.entities import WorkCentersEntity
from data.orm import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey

class WorkCentersModel(BaseModel, WorkCentersEntity):
    __tablename__ = 'work_centers'

    id = Column(Integer, primary_key=True)
    region = Column(String)

    def to_entity(self) -> WorkCentersEntity:
        return WorkCentersEntity(self.region, self.id)