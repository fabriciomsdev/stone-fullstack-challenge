from domain.entities import WorkCentersEntity
from data.models import WorkCentersModel
from utils.patterns import SingletonMeta
from data.data_source import DBDataSource

class WorkCentersRepository(metaclass=SingletonMeta):
    def __init__(self):
        pass

    def _get_DB_session(self, **args):
        return DBDataSource().create_a_session(**args)

    def persist(self, entity: WorkCentersEntity) -> WorkCentersEntity:
        # convert to model
        model = WorkCentersModel(region=entity.region)

        # use SQLAlchemy to persist
        dbSession = self._get_DB_session(expire_on_commit=True)
        dbSession.add(model)
        dbSession.commit()

        #return business entity
        return model.to_entity()

    def get_all(self) -> list:        
        return [model.to_entity() for model in self._get_DB_session().query(WorkCentersModel).all()]
        
    def find(self, primary_key = None) -> WorkCentersEntity:        
        model = self._get_DB_session().query(WorkCentersModel).filter_by(id=primary_key).first()

        if model != None:
            return model.to_entity()
        else:
            return None
