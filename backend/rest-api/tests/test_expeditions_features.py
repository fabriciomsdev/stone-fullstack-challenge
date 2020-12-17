import falcon
from falcon import testing
from tests.utils.datasource_layer import ResetDatabaseEachTestCase
from domain.entities import ExpeditionEntity


class ExpeditionDataAccessTest(ResetDatabaseEachTestCase):

    def test_should_persist_a_expedition(self):
        # repository = ExpeditionsRepository(self._data_source)
        # entity = ExpeditionEntity(qty_of_items=100)

        # repository.persist(entity)
        # repository.save_transaction()
        # qty_of_db_entities = len(repository.fetch())

        # self.assertEqual(qty_of_db_entities, 1)
        pass

    def test_should_cancel_a_expedition(self):
        pass

    def test_should_update_a_expedition(self):
        pass

