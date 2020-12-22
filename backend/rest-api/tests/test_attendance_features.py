import falcon
from falcon import testing
from tests.utils.datasource_layer import ResetDatabaseEachTestCase
from business.domain.entities import AttendanceEntity, WorkCentersEntity
from data.repositories import AttendanceRepository, WorkCentersRepository
from use_cases.attendance import AttendanceUseCases
from utils.exceptions import UseCaseException
from business.messages import AttendanceOperationsRejectionMessages
from tests.utils.application_layer import ResourcesTestCase, ResetAllApplicationEachTestCase
from tests.utils.datasource_layer import ResetDatabaseEachTestCase
from tests.mixins import TestWithWorkCenterCreationMixin
import json
from utils.parses import parse_datetime_to_date_time_str
import datetime


class AttendanceDataAccessTest(ResetDatabaseEachTestCase, TestWithWorkCenterCreationMixin):

    def test_should_persist_a_attendance(self):
        repository = AttendanceRepository(self._data_source)
        work_center_model = self._create_a_work_center_by_data_layer()

        entity = AttendanceEntity(qty_of_terminals=1, work_center=work_center_model)

        repository.persist(entity)
        repository.save_transaction()

        db_entities = repository.fetch()
        calcule_qty_of_terminals_used = WorkCentersRepository(self._data_source).find(work_center_model.id).calcule_qty_of_terminals_used()

        self.assertEqual(len(db_entities), 1)
        self.assertEqual(calcule_qty_of_terminals_used, 1)


    def test_should_cancel_a_attendance(self):
        repository = AttendanceRepository(self._data_source)
        work_center_model = self._create_a_work_center_by_data_layer()

        first_attendance = AttendanceEntity(qty_of_terminals=1, work_center=work_center_model)
        second_attendance = AttendanceEntity(
            qty_of_terminals=1, work_center=work_center_model, was_canceled=True)

        first_attendance = repository.persist(first_attendance)
        second_attendance = repository.persist(second_attendance)
        repository.save_transaction()

        self.assertTrue(second_attendance.was_canceled)


class AttendanceUseCaseTest(ResetDatabaseEachTestCase, TestWithWorkCenterCreationMixin):

    def test_should_create_a_attendance(self):
        repository = AttendanceRepository(self._data_source)
        qty_of_register_in_db_before = len(repository.fetch())
        work_center = self._create_a_work_center_by_data_layer()

        created_entity = AttendanceUseCases(self._data_source).create(AttendanceEntity(
            qty_of_terminals=1,
            work_center=work_center
        ))

        qty_of_register_in_db_after = len(repository.fetch())

        self.assertIsNotNone(created_entity.id)
        self.assertEqual(created_entity.qty_of_terminals, 1)
        self.assertEqual(qty_of_register_in_db_after,
                         qty_of_register_in_db_before + 1)


    def test_can_not_create_a_attendance_without_work_center(self):
        with self.assertRaises(UseCaseException):
            use_case = AttendanceUseCases(self._data_source)
            wrong_data = AttendanceEntity(
                qty_of_terminals=1
            )
            use_case.create(wrong_data)


    def test_can_not_create_a_attendance_without_qty_of_terminals(self):
        work_center_model = self._create_a_work_center_by_data_layer()

        with self.assertRaises(UseCaseException):
            use_case = AttendanceUseCases(self._data_source)
            wrong_data = AttendanceEntity(
                work_center=work_center_model,
                qty_of_terminals = None
            )
            use_case.create(wrong_data)

        with self.assertRaises(UseCaseException):
            use_case = AttendanceUseCases(self._data_source)
            wrong_data = AttendanceEntity(
                work_center=work_center_model,
                qty_of_terminals=0
            )
            use_case.create(wrong_data)


    def test_should_cancel_a_attendance(self):
        work_center = self._create_a_work_center_by_data_layer()
        use_cases = AttendanceUseCases(self._data_source)

        attendance = use_cases.create(AttendanceEntity(
            qty_of_terminals=1,
            work_center=work_center
        ))

        use_cases.cancel_attendance(attendance)

        attendance_updated = use_cases.find(attendance.id)

        self.assertTrue(attendance_updated.was_canceled)


# Application Layer Tests
class AttendanceApplicationLayerTest(ResetAllApplicationEachTestCase, TestWithWorkCenterCreationMixin):

    def test_can_not_block_to_send_a_attendance_with_work_center_blank(self):
        wrong_attendance_data = {
            'qty_of_terminals': 1
        }

        response = self.simulate_post('/attendance', json=wrong_attendance_data)

        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)

    def test_can_not_to_send_a_attendance_with_qty_as_zero(self):
        wrong_attendance_data = {
            'qty_of_terminals': 0
        }

        response = self.simulate_post(
            '/attendance', json=wrong_attendance_data)

        self.assertEqual(response.status, falcon.HTTP_BAD_REQUEST)


    def test_should_register_a_attendance(self):
        work_center_json = self._create_a_work_center_by_application_layer()
        
        attendance_data = {
            'work_center_id': work_center_json['id'],
            'qty_of_terminals': 1
        }

        response = self.simulate_post(
            '/attendance', json=attendance_data)

        self.assertEqual(response.status, falcon.HTTP_CREATED)

    def test_should_cancel_a_attendance(self):
        work_center_json = self._create_a_work_center_by_application_layer()
        attendance_data = {
            'work_center_id': work_center_json['id'],
            'qty_of_terminals': 1
        }
        canceled_attendance_data = {
            'work_center_id': work_center_json['id'],
            'qty_of_terminals': 1,
            'was_canceled': True,
        }

        self.simulate_post(
            '/attendance', json=attendance_data)

        response_update = self.simulate_put(
            '/attendance/1', json=canceled_attendance_data)

        response_get_attendance = self.simulate_get('/attendance/1', headers={
            'content-type': 'application/json'
        })

        response_get_work_center_updated = self.simulate_get('/work-centers/1', headers={
            'content-type': 'application/json'
        })

        work_center_content_updated = json.loads(response_get_work_center_updated.content)
        attendence_on_wc = work_center_content_updated.get("attendance")
        last_attendence_on_wc = attendence_on_wc[0]
        
        self.assertEqual(response_update.status, falcon.HTTP_200)
        self.assertEqual(last_attendence_on_wc.get("was_canceled"), True)
        self.assertEqual(len(attendence_on_wc), 1)
