import falcon
from falcon import testing
from tests.utils.datasource_layer import ResetDatabaseEachTestCase
from domain.entities import ExpeditionsEntity, WorkCentersEntity
from data.repositories import ExpeditionsRepository, WorkCentersRepository
from use_cases.expeditions import ExpeditionsUseCases
from utils.exceptions import UseCaseException
from domain.business_messages import ExpeditionOperationsRejectionMessages
from tests.utils.application_layer import ResourcesTestCase, ResetAllApplicationEachTestCase
from tests.utils.datasource_layer import ResetDatabaseEachTestCase
import json

class TestWithWorkCenterCreationMixin():
    _data_source = None

    def _create_a_work_center_by_data_layer(self):
        work_center_repository = WorkCentersRepository(self._data_source)
        work_center = WorkCentersEntity(region = "SP - Osasco")

        work_center_model = work_center_repository.persist(work_center)
        work_center_repository.save_transaction()

        return work_center_model

    def _create_a_work_center_by_application_layer(self):
        new_work_center_data = {
            'region': "RJ - Rio de Janeiro"
        }

        response = self.simulate_post(
            '/work-centers', json=new_work_center_data)

        return json.loads(response.content)


class ExpeditionDataAccessTest(ResetDatabaseEachTestCase, TestWithWorkCenterCreationMixin):

    def test_should_persist_a_expedition(self):
        repository = ExpeditionsRepository(self._data_source)
        work_center_model = self._create_a_work_center_by_data_layer()

        entity = ExpeditionsEntity(qty_of_items=100, work_center=work_center_model)

        repository.persist(entity)
        repository.save_transaction()

        db_entities = repository.fetch()
        qty_of_terminals_in_wc = work_center_model.to_entity().qty_of_terminals_on_stock()

        self.assertEqual(len(db_entities), 1)
        self.assertEqual(qty_of_terminals_in_wc, 100)


    def test_should_cancel_a_expedition(self):
        repository = ExpeditionsRepository(self._data_source)
        work_center_model = self._create_a_work_center_by_data_layer()

        first_expedition = ExpeditionsEntity(qty_of_items=500, work_center=work_center_model)
        second_expedition = ExpeditionsEntity(qty_of_items=200, work_center=work_center_model)
        third_expedition = ExpeditionsEntity(qty_of_items=200, work_center=work_center_model)

        first_expedition = repository.persist(first_expedition)
        second_expedition = repository.persist(second_expedition)
        third_expedition = repository.persist(third_expedition)
        repository.save_transaction()

        third_expedition.was_canceled = True
        repository.update(third_expedition.to_entity())
        repository.save_transaction()

        qty_in_wc_after_cancel_one = work_center_model.qty_of_terminals_on_stock()

        self.assertEqual(qty_in_wc_after_cancel_one, 700)
        self.assertTrue(third_expedition.was_canceled)


class ExpeditionUseCaseTest(ResetDatabaseEachTestCase, TestWithWorkCenterCreationMixin):

    def test_should_create_a_expedition(self):
        repository = ExpeditionsRepository(self._data_source)
        qty_of_register_in_db_before = len(repository.fetch())
        work_center = self._create_a_work_center_by_data_layer()

        created_entity = ExpeditionsUseCases().create(ExpeditionsEntity(
            qty_of_items=100,
            work_center=work_center
        ))

        qty_of_register_in_db_after = len(repository.fetch())

        self.assertIsNotNone(created_entity.id)
        self.assertEqual(created_entity.qty_of_items, 100)
        self.assertEqual(qty_of_register_in_db_after,
                         qty_of_register_in_db_before + 1)


    def test_can_not_create_a_expedition_without_work_center(self):
        with self.assertRaises(UseCaseException):
            use_case = ExpeditionsUseCases()
            wrong_data = ExpeditionsEntity(
                qty_of_items=100
            )
            use_case.create(wrong_data)


    def test_can_not_create_a_expedition_without_qty_of_items(self):
        work_center_model = self._create_a_work_center_by_data_layer()

        with self.assertRaises(UseCaseException):
            use_case = ExpeditionsUseCases()
            wrong_data = ExpeditionsEntity(
                work_center=work_center_model,
                qty_of_items = None
            )
            use_case.create(wrong_data)

        with self.assertRaises(UseCaseException):
            use_case = ExpeditionsUseCases()
            wrong_data = ExpeditionsEntity(
                work_center=work_center_model,
                qty_of_items=0
            )
            use_case.create(wrong_data)


    def test_should_cancel_a_expedition(self):
        work_center = self._create_a_work_center_by_data_layer()
        use_cases = ExpeditionsUseCases()

        expedition = use_cases.create(ExpeditionsEntity(
            qty_of_items=500,
            work_center=work_center
        ))

        use_cases.cancel_expedition(expedition)

        expedition_updated = use_cases.find(expedition.id)

        self.assertTrue(expedition_updated.was_canceled)

# Application Layer Tests


class ExpeditionApplicationLayerTest(ResetAllApplicationEachTestCase, TestWithWorkCenterCreationMixin):

    def test_can_not_block_to_send_a_expedition_with_work_center_blank(self):
        wrong_expedition_data = {
            'qty_of_items': 100
        }

        response = self.simulate_post('/expeditions', json=wrong_expedition_data)

        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)

    def test_can_not_to_send_a_expedition_with_qty_as_zero(self):
        wrong_expedition_data = {
            'qty_of_items': 0
        }

        response = self.simulate_post(
            '/expeditions', json=wrong_expedition_data)

        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)


    def test_should_send_a_expedition(self):
        work_center_json = self._create_a_work_center_by_application_layer()
        
        expedition_data = {
            'work_center_id': work_center_json['id'],
            'qty_of_items': 1000
        }

        response = self.simulate_post(
            '/expeditions', json=expedition_data)

        self.assertEqual(response.status, falcon.HTTP_CREATED)

    def test_should_cancel_a_expedition(self):
        expected_data = {"id": 1, "qty_of_items": 1000, "was_canceled": True,
                         "work_center": {"region": "RJ - Rio de Janeiro", "id": 1}}
        work_center_json = self._create_a_work_center_by_application_layer()
        expedition_data = {
            'work_center_id': work_center_json['id'],
            'qty_of_items': 1000
        }
        canceled_expedition_data = {
            'work_center_id': work_center_json['id'],
            'qty_of_items': 1000,
            'was_canceled': True,
        }

        self.simulate_post(
            '/expeditions', json=expedition_data)

        response_update = self.simulate_put(
            '/expeditions/1', json=canceled_expedition_data)

        response_get = self.simulate_get('/expeditions/1', headers={
            'content-type': 'application/json'
        })
        
        content_updated = json.loads(response_get.content)
        
        self.assertEqual(response_update.status, falcon.HTTP_200)
        self.assertEqual(content_updated, json.dumps(expected_data))
