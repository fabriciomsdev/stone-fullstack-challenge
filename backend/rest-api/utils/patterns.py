from threading import Lock, Thread
from data.data_source import DBDataSource

class SingletonMeta(type):
    """
    Abstraction of Singleton Thread safe 
    """

    _instance_list = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):

        with cls._lock:
            if cls not in cls._instance_list:
                new_instance = super().__call__(*args, **kwargs)
                cls._instance_list[cls] = new_instance

        return cls._instance_list[cls]


class DBRepository():
    _db_data_source = None

    def __init__(self, db_data_source: DBDataSource):
        self._db_data_source = db_data_source

    def get_db_data_source(self) -> DBDataSource:
        return self._db_data_source


class RepositoryWithUnitOfWork(DBRepository):
    _transaction_session = None

    def __init__(self, db_data_source: DBDataSource):
        super(RepositoryWithUnitOfWork).__init__(db_data_source)
        self._transaction_session = self.get_db_data_source().create_a_session()

    def _define_transaction_session(self):
        self._transaction_session = self.get_db_data_source().create_a_session()

    def _get_transaction_session(self, **args):
        if self._transaction_session == None:
            self._define_transaction_session()

        return self._transaction_session
        
    def save_transaction(self):
        self._get_transaction_session().commit()

    def revert_transaction(self):
        self._get_transaction_session().rollback()


