from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from data.orm import BaseModel
from utils.patterns import Singleton, DataSource
from sqlalchemy import MetaData
import contextlib


class DBDataSource(DataSource, metaclass=Singleton):
    data_base_engine = None

    def _connect_in_database_engine(self, connection_string):
        self.data_base_engine = create_engine(connection_string)
        return self

    def create_database(self):
        BaseModel.metadata.create_all(self.data_base_engine)
        return self

    def connect_to_source(self, connection_string = ''):
        self._connect_in_database_engine(connection_string).create_database()
        return self

    def _truncate_database(self, ignore_foreign_keys = True):
        meta = MetaData(bind=self.data_base_engine, reflect=True)
        con = self.data_base_engine.connect()
        trans = con.begin()

        if ignore_foreign_keys:
            con.execute('SET foreign_key_checks = 0;')

        for table in meta.sorted_tables:
            con.execute(table.delete())

        if ignore_foreign_keys:
            con.execute('SET foreign_key_checks = 1;')

        trans.commit()

    def clear(self, **args):
        self._truncate_database(**args)

    def create_a_session(self, autoflush = False, autocommit = False, expire_on_commit = False):
        Session = sessionmaker(bind=self.data_base_engine, autoflush=autoflush, autocommit=autocommit, expire_on_commit=expire_on_commit)
        return Session()
