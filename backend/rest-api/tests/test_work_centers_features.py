import falcon
from falcon import testing
import unittest
import json

from tests.utils.application_layer import ResourcesTestCase, ResetAllApplicationEachTestCase
from tests.utils.datasource_layer import ResetDatabaseEachTestCase

from service.start import ApplicationBuilder, app
from use_cases.work_centers import WorkCentersUseCases
from domain.entities import WorkCentersEntity
from data.repositories import WorkCentersRepository
from domain.business_rules import WorkCenterBusinessRules
from domain.coverage_classification import CoverageClassifications


# Data Manipulation Tests
class WorkCenterDataAccessTest(ResetDatabaseEachTestCase):

    def test_should_persist_a_work_center_in_db(self):
        repository = WorkCentersRepository(self._data_source)
        qty_of_entities_in_db_before = len(repository.fetch())

        entity = WorkCentersEntity(region = "SP - São Paulo")
        repository.persist(entity)
        repository.save_transaction()

        qty_of_entities_in_db_after = len(repository.fetch())

        self.assertNotEqual(qty_of_entities_in_db_before, qty_of_entities_in_db_after)

    def test_should_get_all_work_centers_in_db(self):
        repository = WorkCentersRepository(self._data_source)

        entity_SP = WorkCentersEntity(region = "SP - São Paulo")
        entity_RJ = WorkCentersEntity(region = "RJ - Rio de Janeiro")
        entity_BH = WorkCentersEntity(region = "BH - Belo Horizonte")

        repository.persist(entity_SP)
        repository.persist(entity_RJ)
        repository.persist(entity_BH)
        repository.save_transaction()

        entities_on_db = repository.fetch()

        self.assertEqual(len(entities_on_db), 3)

    def test_should_get_one_work_center_in_db(self):
        repository = WorkCentersRepository(self._data_source)
        entity_SP = WorkCentersEntity(region = "SP - São Paulo")
        
        entity = repository.persist(entity_SP)
        repository.save_transaction()
        
        all_entities = repository.fetch()
        last_entity_added = all_entities[len(all_entities) - 1]

        self.assertEqual(entity.region, last_entity_added.region)
        self.assertIsNotNone(last_entity_added.id)

    def test_should_delete_one_work_center_in_db(self):
        entity_SP = WorkCentersEntity(region = "SP - São Paulo")
        repository = WorkCentersRepository(self._data_source)

        entity = repository.persist(entity_SP)
        repository.save_transaction()

        repository.delete(entity)
        repository.save_transaction()

        found_entity = repository.find(entity.id)

        self.assertIsNone(found_entity)

    def test_should_update_one_work_center_in_db(self):
        entity_SP = WorkCentersEntity(region = "SP - São Paulo")
        repository = WorkCentersRepository(self._data_source)
        new_name = "SP - São Paulo 2"

        entity = repository.persist(entity_SP)
        repository.save_transaction()

        entity.region = new_name

        repository.update(entity)
        repository.save_transaction()

        self.assertEqual(entity.region, new_name)



# BusinessRules Tests
class WorkCenterBusinessRulesTest(unittest.TestCase):
    rules = WorkCenterBusinessRules()

    def test_should_invalid_a_work_center_without_region(self):
        wc_empty = WorkCentersEntity()
        wc_without_region = WorkCentersEntity(**{'region': ''})

        res_of_wc_empty = self.rules.is_not_a_valid_work_center_data_to_register(wc_empty)
        res_of_wc_without_region = self.rules.is_not_a_valid_work_center_data_to_register(wc_without_region)

        self.assertEqual(res_of_wc_empty, True)
        self.assertEqual(res_of_wc_without_region, True)


# Use Cases Tests (Business Layer)
class WorkCenterUseCasesTest(ResetDatabaseEachTestCase):
    def test_should_create_a_work_center_and_return_data_from_db(self):
        repository = WorkCentersRepository(self._data_source)
        qty_of_register_in_db_before = len(repository.fetch())

        created_entity = WorkCentersUseCases().create(WorkCentersEntity(region = "SP - São Paulo"))

        qty_of_register_in_db_after = len(repository.fetch())

        self.assertIsNotNone(created_entity.id)
        self.assertEqual(created_entity.region, "SP - São Paulo")
        self.assertEqual(qty_of_register_in_db_after, qty_of_register_in_db_before + 1)

    def test_should_get_all_work_centers(self):
        WorkCentersUseCases().create(WorkCentersEntity(region = "SP - São Paulo"))
        WorkCentersUseCases().create(WorkCentersEntity(region = "RJ - Rio de Janeiro"))
        WorkCentersUseCases().create(WorkCentersEntity(region = "BH - Belo Horizonte"))
        
        work_centers = WorkCentersUseCases().get_all()
        self.assertEqual(len(work_centers), 3)

    def test_should_find_a_work_center(self):
        created_entity = WorkCentersUseCases().create(WorkCentersEntity(region = "SP - São Paulo"))
        found_entity = WorkCentersUseCases().find(created_entity.id)

        self.assertEqual(found_entity.id, created_entity.id)

    def test_should_delete_a_work_center(self):
        created_entity = WorkCentersUseCases().create(WorkCentersEntity(region = "SP - São Paulo"))
        WorkCentersUseCases().delete(created_entity)
        found_entity = WorkCentersUseCases().find(created_entity.id)

        self.assertIsNone(found_entity)

    def test_should_update_a_work_center(self):
        new_region = "RJ - Rio de Janeiro - Madureira"
        created_entity = WorkCentersUseCases().create(WorkCentersEntity(region = "SP - São Paulo"))
        
        created_entity.region = new_region
        WorkCentersUseCases().update(created_entity)

        found_entity = WorkCentersUseCases().find(created_entity.id)

        self.assertEqual(found_entity.region, new_region)


        

# Application Layer Tests
class WorkCenterApplicationLayerTest(ResetAllApplicationEachTestCase):

    def test_should_block_to_create_a_work_center_with_region_blank(self):
        new_work_center_data = {
            'region': ""
        }

        response = self.simulate_post('/work-centers', json=new_work_center_data)

        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)


    def test_should_block_to_create_a_invalid_work_center_none(self):
        new_work_center_data = {
            'region': None
        }

        response = self.simulate_post('/work-centers', json=new_work_center_data)

        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)


    def test_should_create_a_work_center(self):
        new_work_center_data = {
            'region': "RJ - Rio de Janeiro"
        }

        response = self.simulate_post('/work-centers', json=new_work_center_data)
        
        self.assertEqual(response.status, falcon.HTTP_CREATED)

    
    def test_should_get_all_work_centers_data(self):
        expected_data = [
            {
                "id": 1,
                "region": "RJ - Rio de Janeiro",
                "expeditions": [],
                "attendance": [],
                "days_qty_ideal_for_coverage": 14,
                "qty_of_terminals_used": 0,
                "qty_of_terminals_received": 0,
                "qty_of_terminals_available": 0,
                "avg_of_attendence": 0,
                "coverage_classification": CoverageClassifications.RED
            },
            {
                "id": 2,
                "region": "SP - Osasco",
                "expeditions": [],
                "attendance": [],
                "days_qty_ideal_for_coverage": 14,
                "qty_of_terminals_used": 0,
                "qty_of_terminals_received": 0,
                "qty_of_terminals_available": 0,
                "avg_of_attendence": 0,
                "coverage_classification": CoverageClassifications.RED
            }
        ]

        self.simulate_post('/work-centers', json={
            'region': "RJ - Rio de Janeiro"
        })

        self.simulate_post('/work-centers', json={
            'region': "SP - Osasco"
        })
        
        response = self.simulate_get('/work-centers', headers = {
            'content-type': 'application/json'
        })
        
        response_data = [json.loads(item) for item in json.loads(response.content)]

        self.assertEqual(response.status, falcon.HTTP_OK)
        self.assertListEqual(response_data, expected_data)


    def test_should_get_one_work_center_data(self):
        expected_data = {
            "id": 1,
            "region": "RJ - Rio de Janeiro",
            "attendance": [],
            "expeditions": [],
            "days_qty_ideal_for_coverage": 14,
            "qty_of_terminals_used": 0,
            "qty_of_terminals_received": 0,
            "qty_of_terminals_available": 0,
            "avg_of_attendence": 0,
            "coverage_classification": CoverageClassifications.RED
        }

        self.simulate_post('/work-centers', json={
            'region': "RJ - Rio de Janeiro"
        })

        response = self.simulate_get('/work-centers/1')
        
        received_data = json.loads(json.loads(response.content))

        self.assertEqual(response.status, falcon.HTTP_200)
        self.assertEqual(received_data, expected_data)
        

    def test_should_not_get_one_work_center_data_and_return_404(self):
        response = self.simulate_get('/work-centers/1')

        self.assertEqual(response.status, falcon.HTTP_404)

    def test_should_delete_one_work_center_data(self):
        self.simulate_post('/work-centers', json={
            'region': "RJ - Rio de Janeiro"
        })

        response = self.simulate_delete('/work-centers/1')

        self.assertEqual(response.status, falcon.HTTP_200)

    def test_should_update_one_work_center_data(self):
        self.simulate_post('/work-centers', json={
            'region': "RJ - Rio de Janeiro"
        })

        response = self.simulate_put('/work-centers/1', json={
            'region': "RJ - Rio de Janeiro 4"
        })

        self.assertEqual(response.status, falcon.HTTP_200)

