from domain.entities import WorkCentersEntity
from data.models import WorkCentersModel
from utils.patterns import SingletonMeta
from data.data_source import DBDataSource

class WorkCentersRepository(metaclass=SingletonMeta):
    def __init__(self):
        pass

    def persist(self, entity: WorkCentersEntity) -> WorkCentersEntity:
        # convert to model
        model = WorkCentersModel(region=entity.region)

        # use SQLAlchemy to persist
        dbSession = DBDataSource().create_a_session()
        dbSession.add(model)
        dbSession.commit()
        dbSession.close()

        #return business entity
        return model.to_entity()