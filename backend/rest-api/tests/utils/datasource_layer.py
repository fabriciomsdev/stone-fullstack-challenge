from data.data_source import DBDataSource
import unittest

class ResetDatabaseEachTestCase(unittest.TestCase):
    _data_source = None
    
    def setUp(self):
        self._data_source = DBDataSource()
        self._data_source.connect_to_source('sqlite:///db.sqlite3')
        self._data_source.clear(ignore_foreign_keys=False)

    def tearDown(self):
        self._data_source.clear(ignore_foreign_keys=False)
