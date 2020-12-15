import falcon
from falcon import testing
import pytest
from service.start import ApplicationBuilder, app
from urllib.parse import urlencode
import json
from domain.business_rules import WorkCenterBusinessValidationsRules
import unittest
from tests.utils.application_layer import ResourcesTestCase, ResetAllApplicationEachTestCase
from tests.utils.datasource_layer import ResetDatabaseEachTestCase
from use_cases.work_centers import WorkCentersUseCases
from domain.entities import WorkCentersEntity
from data.repositories import WorkCentersRepository
from data.data_source import DBDataSource


# Data Manipulation Tests
class WorkCenterDataAccessTest(ResetDatabaseEachTestCase):

    def test_should_persist_a_work_center_in_db(self):
        qty_of_entities_in_db_before = len(WorkCentersRepository().get_all())

        entity = WorkCentersEntity(region = "SP - São Paulo")
        WorkCentersRepository().persist(entity)

        qty_of_entities_in_db_after = len(WorkCentersRepository().get_all())

        self.assertNotEqual(qty_of_entities_in_db_before, qty_of_entities_in_db_after)

    def test_should_get_all_work_centers_in_db(self):
        qty_of_entities_in_db_before = len(WorkCentersRepository().get_all())
        repository = WorkCentersRepository()

        entity_SP = WorkCentersEntity(region = "SP - São Paulo")
        entity_RJ = WorkCentersEntity(region = "RJ - Rio de Janeiro")
        entity_BH = WorkCentersEntity(region = "BH - Belo Horizonte")

        repository.persist(entity_SP)
        repository.persist(entity_RJ)
        repository.persist(entity_BH)

        entities_on_db = WorkCentersRepository().get_all()

        self.assertEqual(len(entities_on_db), 3)

    def test_should_get_one_work_center_in_db(self):
        entity_SP = WorkCentersEntity(region = "SP - São Paulo")
        repository = WorkCentersRepository()
        
        entity = repository.persist(entity_SP)

        found_entity = repository.find(entity.id)

        self.assertEqual(entity.id, found_entity.id)
        self.assertEqual(entity.region, found_entity.region)



# BusinessRules Tests
class WorkCenterBusinessRulesTest(unittest.TestCase):
    def test_should_invalid_a_work_center_without_region(self):
        assert WorkCenterBusinessValidationsRules().is_not_a_valid_work_center_data_to_register(WorkCentersEntity()) == True
        assert WorkCenterBusinessValidationsRules().is_not_a_valid_work_center_data_to_register(WorkCentersEntity(**{'region' : ''})) == True


# Use Cases Tests (Business Layer)
class WorkCenterUseCasesTest(ResetDatabaseEachTestCase):
    def test_should_create_a_work_center_and_return_data_from_db(self):
        qty_of_register_in_db_before = len(WorkCentersRepository().get_all())
        created_entity = WorkCentersUseCases().create(WorkCentersEntity(region = "SP - São Paulo"))
        qty_of_register_in_db_after = len(WorkCentersRepository().get_all())

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
        self.simulate_post('/work-centers', json={
            'region': "RJ - Rio de Janeiro"
        })

        self.simulate_post('/work-centers', json={
            'region': "SP - São Paulo"
        })
        
        response = self.simulate_get('/work-centers', headers = {
            'content-type': 'application/json'
        })

        self.assertEqual(response.status, falcon.HTTP_OK)
        response_data = [json.loads(item) for item in json.loads(response.content)]
        expected_data = [{
            "id": 1,
            "region": "RJ - Rio de Janeiro"
        }, 
        {
            "id": 2,
            "region": "SP - São Paulo"
        }]

        self.assertEqual(response_data, expected_data)


    def test_should_get_one_work_center_data(self):
        self.simulate_post('/work-centers', json={
            'region': "RJ - Rio de Janeiro"
        })

        expected_data = {
            'id': 1,
            'region': "RJ - Rio de Janeiro"
        }

        response = self.simulate_get('/work-centers/1')

        self.assertEqual(response.status, falcon.HTTP_200)
        
        received_data = json.loads(response.content)

        self.assertEqual(received_data, json.dumps(expected_data))
        

    def test_should_not_get_one_work_center_data_and_return_404(self):
        response = self.simulate_get('/work-centers/1')

        self.assertEqual(response.status, falcon.HTTP_404)

