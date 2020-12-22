import falcon
from falcon import testing
from tests.utils.datasource_layer import ResetDatabaseEachTestCase
from business.domain.entities import ExpeditionsEntity, WorkCentersEntity
from data.repositories import ExpeditionsRepository, WorkCentersRepository
from use_cases.expeditions import ExpeditionsUseCases
from utils.exceptions import UseCaseException
from business.messages import ExpeditionOperationsRejectionMessages
from tests.utils.application_layer import ResourcesTestCase, ResetAllApplicationEachTestCase
from tests.utils.datasource_layer import ResetDatabaseEachTestCase
from tests.mixins import TestWithWorkCenterCreationMixin
import json
from business.domain.coverage_classification import CoverageClassifications


class ExpeditionDataAccessTest(ResetDatabaseEachTestCase, TestWithWorkCenterCreationMixin):

    def test_should_persist_a_expedition(self):
        repository = ExpeditionsRepository(self._data_source)
        work_center_model = self._create_a_work_center_by_data_layer()

        entity = ExpeditionsEntity(qty_of_terminals=100, work_center=work_center_model)

        repository.persist(entity)
        repository.save_transaction()

        db_entities = repository.fetch()
        qty_of_terminals_in_wc = work_center_model.to_entity().calcule_qty_of_terminals_received()

        self.assertEqual(len(db_entities), 1)
        self.assertEqual(qty_of_terminals_in_wc, 100)


    def test_should_cancel_a_expedition(self):
        repository = ExpeditionsRepository(self._data_source)
        work_center_model = self._create_a_work_center_by_data_layer()

        first_expedition = ExpeditionsEntity(qty_of_terminals=500, work_center=work_center_model)
        second_expedition = ExpeditionsEntity(qty_of_terminals=200, work_center=work_center_model, was_canceled=True)

        first_expedition = repository.persist(first_expedition)
        second_expedition = repository.persist(second_expedition)
        repository.save_transaction()

        qty_in_wc_after_cancel_one = work_center_model.calcule_qty_of_terminals_received()

        self.assertEqual(qty_in_wc_after_cancel_one, 500)
        self.assertTrue(second_expedition.was_canceled)


class ExpeditionUseCaseTest(ResetDatabaseEachTestCase, TestWithWorkCenterCreationMixin):

    def test_should_create_a_expedition(self):
        repository = ExpeditionsRepository(self._data_source)
        qty_of_register_in_db_before = len(repository.fetch())
        work_center = self._create_a_work_center_by_data_layer()

        created_entity = ExpeditionsUseCases(self._data_source).create(ExpeditionsEntity(
            qty_of_terminals=100,
            work_center=work_center
        ))

        qty_of_register_in_db_after = len(repository.fetch())

        self.assertIsNotNone(created_entity.id)
        self.assertEqual(created_entity.qty_of_terminals, 100)
        self.assertEqual(qty_of_register_in_db_after,
                         qty_of_register_in_db_before + 1)


    def test_can_not_create_a_expedition_without_work_center(self):
        with self.assertRaises(UseCaseException):
            use_case = ExpeditionsUseCases(self._data_source)
            wrong_data = ExpeditionsEntity(
                qty_of_terminals=100
            )
            use_case.create(wrong_data)


    def test_can_not_create_a_expedition_without_qty_of_terminals(self):
        work_center_model = self._create_a_work_center_by_data_layer()

        with self.assertRaises(UseCaseException):
            use_case = ExpeditionsUseCases(self._data_source)
            wrong_data = ExpeditionsEntity(
                work_center=work_center_model,
                qty_of_terminals = None
            )
            use_case.create(wrong_data)

        with self.assertRaises(UseCaseException):
            use_case = ExpeditionsUseCases(self._data_source)
            wrong_data = ExpeditionsEntity(
                work_center=work_center_model,
                qty_of_terminals=0
            )
            use_case.create(wrong_data)


    def test_should_cancel_a_expedition(self):
        work_center = self._create_a_work_center_by_data_layer()
        use_cases = ExpeditionsUseCases(self._data_source)

        expedition = use_cases.create(ExpeditionsEntity(
            qty_of_terminals=500,
            work_center=work_center
        ))

        use_cases.cancel_expedition(expedition)

        expedition_updated = use_cases.find(expedition.id)

        self.assertTrue(expedition_updated.was_canceled)

# Application Layer Tests


class ExpeditionApplicationLayerTest(ResetAllApplicationEachTestCase, TestWithWorkCenterCreationMixin):

    def test_can_not_block_to_send_a_expedition_with_work_center_blank(self):
        wrong_expedition_data = {
            'qty_of_terminals': 100
        }

        response = self.simulate_post('/expeditions', json=wrong_expedition_data)

        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)

    def test_can_not_to_send_a_expedition_with_qty_as_zero(self):
        wrong_expedition_data = {
            'qty_of_terminals': 0
        }

        response = self.simulate_post(
            '/expeditions', json=wrong_expedition_data)

        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)


    def test_should_send_a_expedition_by_request(self):
        work_center_json = self._create_a_work_center_by_application_layer()
        
        expedition_data = {
            'work_center_id': work_center_json.get('id'),
            'qty_of_terminals': 1000
        }

        response = self.simulate_post(
            '/expeditions', json=expedition_data)
        
        self.assertEqual(response.status, falcon.HTTP_CREATED)

    def test_should_cancel_a_expedition_by_request(self):
        expected_expedition_data = {
            "auto_predict_qty_needed": False,
            "id": 1, 
            "qty_of_terminals": 1000, 
            "was_canceled": True,
            "work_center": { 
                'avg_of_attendence': 0, 
                'coverage_classification': 'Vermelha', 
                'days_of_coverage': 0, 
                'days_qty_ideal_for_coverage': 14, 
                'id': 1, 
                'qty_of_terminals_available': 0, 
                'qty_of_terminals_received': 0, 
                'qty_of_terminals_used': 0, 
                'region': 'RJ - Rio de Janeiro'
            }
        }
        expected_work_center_data = {
            "attendance": [],
            "avg_of_attendence": 0,
            "days_qty_ideal_for_coverage": 14,
            "coverage_classification": "Vermelha",
            "days_of_coverage": 0,
            "expeditions": [
                {
                    "auto_predict_qty_needed": False,
                    "id": 1,
                    "qty_of_terminals": 1000,
                    "was_canceled": True,
                }
            ],
            "id": 1, 
            "qty_of_terminals_available": 0,
            "qty_of_terminals_received": 0,
            "qty_of_terminals_used": 0,
            "region": "RJ - Rio de Janeiro"
        }
        work_center_json = self._create_a_work_center_by_application_layer()
        expedition_data = {
            'work_center_id': work_center_json['id'],
            'qty_of_terminals': 1000
        }
        canceled_expedition_data = {
            'work_center_id': work_center_json['id'],
            'qty_of_terminals': 1000,
            'was_canceled': True,
        }

        self.simulate_post(
            '/expeditions', json=expedition_data)

        response_update = self.simulate_put(
            '/expeditions/1', json=canceled_expedition_data)

        response_get_expedition = self.simulate_get('/expeditions/1', headers={
            'content-type': 'application/json'
        })

        response_get_work_center_updated = self.simulate_get('/work-centers/1', headers={
            'content-type': 'application/json'
        })

        expedition_content_updated = response_get_expedition.json
        work_center_content_updated = response_get_work_center_updated.json

        work_center_content_updated = work_center_content_updated
        expedition_content_updated = expedition_content_updated

        self.assertEqual(response_update.status, falcon.HTTP_200)

        self.assertEqual(expedition_content_updated,
                         expected_expedition_data)

        self.assertEqual(work_center_content_updated,
                         expected_work_center_data)
