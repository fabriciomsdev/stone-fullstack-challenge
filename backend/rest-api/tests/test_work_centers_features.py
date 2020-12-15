import falcon
from falcon import testing
import pytest
from service.start import ApplicationBuilder, app
from urllib.parse import urlencode
import json
from domain.business_rules import WorkCenterBusinessValidationsRules
import unittest
from tests.utils.resources import ResourcesTestCase
from use_cases.work_centers import CreateAWorkCentersUseCase
from domain.entities import WorkCentersEntity
from data.repositories import WorkCentersRepository

# BusinessRules Tests
class WorkCenterBusinessRulesTest(unittest.TestCase):
    def test_should_invalid_a_work_center_without_region(self):
        assert WorkCenterBusinessValidationsRules().is_not_a_valid_work_center_data_to_register(WorkCentersEntity()) == True
        assert WorkCenterBusinessValidationsRules().is_not_a_valid_work_center_data_to_register(WorkCentersEntity(**{'region' : ''})) == True


# Use Cases Tests
class WorkCenterUseCasesTest(unittest.TestCase):
    def setUp(self):
        ApplicationBuilder().create_and_start_database()

    def test_create_a_work_center_and_return_data_from_db(self):
        qty_of_register_in_db_before = len(WorkCentersRepository().get_all())
        created_entity = CreateAWorkCentersUseCase().execute(WorkCentersEntity(region = "SP - São Paulo"))
        qty_of_register_in_db_after = len(WorkCentersRepository().get_all())

        self.assertIsNotNone(created_entity.id)
        self.assertEqual(created_entity.region, "SP - São Paulo")
        self.assertEqual(qty_of_register_in_db_after, qty_of_register_in_db_before + 1)


# Application Layer Tests
class WorkCenterResourceTest(ResourcesTestCase):

    def test_block_to_create_a_work_center_with_region_blank(self):
        new_work_center_data = {
            'region': ""
        }

        response = self.simulate_post('/work-centers', json=new_work_center_data)

        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)


    def test_block_to_create_a_invalid_work_center_none(self):
        new_work_center_data = {
            'region': None
        }

        response = self.simulate_post('/work-centers', json=new_work_center_data)

        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)


    def test_create_a_work_center(self):
        new_work_center_data = {
            'region': "RJ - Rio de Janeiro"
        }

        response = self.simulate_post('/work-centers', json=new_work_center_data)

        self.assertEqual(response.status, falcon.HTTP_CREATED)

