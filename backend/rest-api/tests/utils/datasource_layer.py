from data.data_source import DBDataSource
import unittest

class ResetDatabaseEachTestCase(unittest.TestCase):
    def setUp(self):
        DBDataSource().build('sqlite:///db.sqlite3')
        DBDataSource().clear(ignore_foreign_keys = False)

    def tearDown(self):
        DBDataSource().clear(ignore_foreign_keys = False)