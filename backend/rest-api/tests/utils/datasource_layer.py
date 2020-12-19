from data.data_source import DBDataSource
import unittest
import time
import environ

class ResetDatabaseEachTestCase(unittest.TestCase):
    _data_source: DBDataSource = DBDataSource()
    
    def setUp(self):
        self._data_source.connect_to_source('sqlite:///db.sqlite3')
        self._data_source.clear(ignore_foreign_keys=False)
        time.sleep(0.05)

    def tearDown(self):
        self._data_source.clear(ignore_foreign_keys=False)
        time.sleep(0.05)
