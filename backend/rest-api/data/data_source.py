from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from data.orm import BaseModel
from utils.patterns import SingletonMeta

class DBDataSource(metaclass=SingletonMeta):
    data_source_engine = None

    def connect_in_database_engine(self, connection_string):
        self.data_source_engine = create_engine(connection_string)
        return self

    def create_database(self):
        BaseModel.metadata.create_all(self.data_source_engine)
        return self

    def build(self, connection_string = ''):
        self.connect_in_database_engine(connection_string).create_database()
        return self

    def create_a_session(self, autoflush = False, autocommit = False, expire_on_commit = False):
        Session = sessionmaker(bind=self.data_source_engine, autoflush=autoflush, autocommit=autocommit, expire_on_commit=expire_on_commit)
        return Session()