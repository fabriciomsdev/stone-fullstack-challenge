from threading import Lock, Thread

class SingletonMultiThread(type):
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


class Singleton(type):
    """
    Abstraction of Singleton
    """
    _instance_list = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance_list:
            instance = super().__call__(*args, **kwargs)
            cls._instance_list[cls] = instance
        return cls._instance_list[cls]


class DataSource(object):
    def connect_to_source(self):
        pass


class DBRepository(object):
    _db_data_source = None

    def __init__(self, db_data_source: DataSource):
        self._db_data_source = db_data_source

    def get_db_data_source(self) -> DataSource:
        return self._db_data_source


class RepositoryWithUnitOfWork(DBRepository):
    _transaction_session = None

    def __init__(self, db_data_source: DataSource):
        super(RepositoryWithUnitOfWork, self).__init__(db_data_source)
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


