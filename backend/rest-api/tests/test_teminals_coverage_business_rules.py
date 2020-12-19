# Data Manipulation Tests
from data.repositories import WorkCentersRepository
from domain.entities import AttendanceEntity, ExpeditionsEntity, WorkCentersEntity
from tests.utils.datasource_layer import ResetDatabaseEachTestCase
from use_cases.work_centers import WorkCentersUseCases
from use_cases.attendance import AttendanceUseCases
import datetime
import random
from use_cases.expeditions import ExpeditionsUseCases
from domain.business_rules import WorkCenterBusinessRules
from asyncio.tasks import sleep
from domain.coverage_classification import CoverageClassifications
import time

class WorkCenterBusinessCoverage(ResetDatabaseEachTestCase):
    _fake_wc_entity = WorkCentersEntity(region="SP - São Paulo")

    def _get_date_days_ago(self, days_ago = 14):
        param_date = datetime.datetime.now()
        days_to_discount = datetime.timedelta(days_ago)

        new_date = param_date - days_to_discount

        return new_date

    def test_should_get_right_average_of_attendence(self):
        days_used_in_avg = 14
        use_cases = WorkCentersUseCases()
        work_center = use_cases.create(self._fake_wc_entity)
        avg_before = use_cases.get_average_of_attendences_in_wc(
            work_center, days_used_in_avg)

        list_of_attendences = [
            AttendanceEntity(qty_of_terminals=1, work_center=work_center),
            AttendanceEntity(qty_of_terminals=1, work_center=work_center,
                             attendance_date=self._get_date_days_ago(7)),
            AttendanceEntity(qty_of_terminals=1, work_center=work_center,
                             attendance_date=self._get_date_days_ago(10)),
            AttendanceEntity(qty_of_terminals=1, work_center=work_center, was_canceled=True),
        ]

        for attdc in list_of_attendences:
            attdc = AttendanceUseCases().create(attdc)

        avg_after = use_cases.get_average_of_attendences_in_wc(
            work_center, days_used_in_avg)

        self.assertEqual(avg_before, 0)
        self.assertEqual(avg_after, 3)


    def test_is_getting_right_green_classification_of_coverage(self):
        days_used_in_avg = 14
        use_cases = WorkCentersUseCases()
        work_center = use_cases.create(self._fake_wc_entity)
        business_rules = WorkCenterBusinessRules()

        self._register_fake_attendences_in(work_center, 250, days_used_in_avg)
        self._register_fake_expeditions_in(work_center, 20, 25)

        work_center_updated = use_cases.find(work_center.id)

        terminals_used = work_center_updated.calcule_qty_of_terminals_used()
        terminals_received = work_center_updated.calcule_qty_of_terminals_received()
        terminails_available = business_rules.get_qty_of_terminals_available(
            work_center_updated)
        avg_attendance = use_cases.get_average_of_attendences_in_wc(
            work_center_updated, days_used_in_avg)

        classfication = business_rules.get_coverage_classification(
            terminails_available, avg_attendance, days_used_in_avg)

        self.assertEqual(terminals_used, 250)
        self.assertEqual(terminals_received, 500)
        self.assertEqual(avg_attendance, 17)
        self.assertEqual(classfication, CoverageClassifications.GREEN)

    def test_is_getting_right_red_with_low_stock_classification_of_coverage(self):
        days_used_in_avg = 14
        use_cases = WorkCentersUseCases()
        work_center = use_cases.create(self._fake_wc_entity)
        business_rules = WorkCenterBusinessRules()

        self._register_fake_attendences_in(work_center, 75, days_used_in_avg)
        self._register_fake_expeditions_in(work_center, 9, 10)

        work_center_updated = use_cases.find(work_center.id)

        terminals_used = work_center_updated.calcule_qty_of_terminals_used()
        terminals_received = work_center_updated.calcule_qty_of_terminals_received()
        terminails_available = business_rules.get_qty_of_terminals_available(
            work_center_updated)
        avg_attendance = use_cases.get_average_of_attendences_in_wc(
            work_center_updated, days_used_in_avg)


        classfication = business_rules.get_coverage_classification(
            terminails_available, avg_attendance, days_used_in_avg)
        days_coverage = business_rules.get_days_coverage(
            terminails_available, avg_attendance)

        self.assertEqual(terminals_used, 75)
        self.assertEqual(terminals_received, 90)
        self.assertEqual(days_coverage, 3)
        self.assertEqual(classfication, CoverageClassifications.RED)

    def test_is_getting_right_red_with_high_stock_classification_of_coverage(self):
        days_used_in_avg = 14
        use_cases = WorkCentersUseCases()
        work_center = use_cases.create(self._fake_wc_entity)
        business_rules = WorkCenterBusinessRules()

        self._register_fake_attendences_in(work_center, 75, days_used_in_avg)
        self._register_fake_expeditions_in(work_center, 30, 10)
        time.sleep(1)
        
        work_center_updated = use_cases.find(work_center.id)

        terminals_used = work_center_updated.calcule_qty_of_terminals_used()
        terminals_received = work_center_updated.calcule_qty_of_terminals_received()
        terminails_available = business_rules.get_qty_of_terminals_available(
            work_center_updated)
        avg_attendance = use_cases.get_average_of_attendences_in_wc(
            work_center_updated, days_used_in_avg)

        classfication = business_rules.get_coverage_classification(
            terminails_available, avg_attendance, days_used_in_avg)
        days_coverage = business_rules.get_days_coverage(
            terminails_available, avg_attendance)

        self.assertEqual(terminals_used, 75)
        self.assertEqual(terminals_received, 300)
        self.assertGreater(days_coverage, 23)
        self.assertEqual(classfication, CoverageClassifications.RED)

    def test_is_getting_right_yellow_with_low_stock_classification_of_coverage(self):
        days_used_in_avg = 14
        use_cases = WorkCentersUseCases()
        work_center = use_cases.create(self._fake_wc_entity)
        business_rules = WorkCenterBusinessRules()

        self._register_fake_attendences_in(work_center, 75, days_used_in_avg)
        self._register_fake_expeditions_in(work_center, 13, 10)
        time.sleep(1)

        work_center_updated = use_cases.find(work_center.id)

        terminals_used = work_center_updated.calcule_qty_of_terminals_used()
        terminals_received = work_center_updated.calcule_qty_of_terminals_received()
        terminails_available = business_rules.get_qty_of_terminals_available(
            work_center_updated)

        avg_attendance = use_cases.get_average_of_attendences_in_wc(
            work_center_updated, days_used_in_avg)
        classfication = business_rules.get_coverage_classification(
            terminails_available, avg_attendance, days_used_in_avg)
        days_coverage = business_rules.get_days_coverage(
            terminails_available, avg_attendance)

        self.assertEqual(terminals_used, 75)
        self.assertEqual(terminals_received, 130)
        self.assertGreaterEqual(days_coverage, 10)
        self.assertLessEqual(days_coverage, 13)
        self.assertEqual(classfication, CoverageClassifications.YELLOW)


    def test_is_getting_right_yellow_with_high_stock_classification_of_coverage(self):
        days_used_in_avg = 14
        use_cases = WorkCentersUseCases()
        work_center = use_cases.create(self._fake_wc_entity)
        business_rules = WorkCenterBusinessRules()

        self._register_fake_attendences_in(work_center, 75, days_used_in_avg)
        self._register_fake_expeditions_in(work_center, 19, 10)
        time.sleep(1)

        work_center_updated = use_cases.find(work_center.id)

        terminals_used = work_center_updated.calcule_qty_of_terminals_used()
        terminals_received = work_center_updated.calcule_qty_of_terminals_received()
        terminails_available = business_rules.get_qty_of_terminals_available(
            work_center_updated)

        avg_attendance = use_cases.get_average_of_attendences_in_wc(
            work_center_updated, days_used_in_avg)
        classfication = business_rules.get_coverage_classification(
            terminails_available, avg_attendance, days_used_in_avg)
        days_coverage = business_rules.get_days_coverage(
            terminails_available, avg_attendance)

        self.assertEqual(terminals_used, 75)
        self.assertEqual(terminals_received, 190)
        self.assertGreaterEqual(days_coverage, 19)
        self.assertLessEqual(days_coverage, 23)
        self.assertEqual(classfication, CoverageClassifications.YELLOW)

    def test_is_getting_right_qty_of_terminals_in_send_auto_predict_expeditions(self):
        use_cases = WorkCentersUseCases()
        work_center = use_cases.create(self._fake_wc_entity)
        business_rules = WorkCenterBusinessRules()
        expedition_use_case = ExpeditionsUseCases()

        self._register_fake_attendences_in(work_center, 75, work_center.days_qty_ideal_for_coverage)
        self._register_fake_expeditions_in(work_center, 9, 10)

        work_center_updated = use_cases.find(work_center.id)

        terminails_available_before = business_rules.get_qty_of_terminals_available(
            work_center_updated)
        avg_attendance = use_cases.get_average_of_attendences_in_wc(
            work_center_updated, work_center.days_qty_ideal_for_coverage)

        classfication_before = business_rules.get_coverage_classification(
            terminails_available_before, avg_attendance, work_center.days_qty_ideal_for_coverage)

        expedition = expedition_use_case.create(ExpeditionsEntity(
            work_center=work_center,
            auto_predict_qty_needed=True
        ))
        
        # Atualizando dados do work_center
        work_center_updated = use_cases.find(work_center.id)

        terminails_available = business_rules.get_qty_of_terminals_available(
            work_center_updated)
        
        avg_attendance = use_cases.get_average_of_attendences_in_wc(
            work_center_updated, work_center.days_qty_ideal_for_coverage)
        classfication_after = business_rules.get_coverage_classification(
            terminails_available, avg_attendance, work_center.days_qty_ideal_for_coverage)

        self.assertEqual(classfication_before, CoverageClassifications.RED)
        self.assertEqual(classfication_after, CoverageClassifications.GREEN)


    def _register_fake_attendences_in(self, work_center: WorkCentersEntity, qty_of_attendence: int = 5, days_limit: int = 14):
        while len(AttendanceUseCases().get_all()) < qty_of_attendence:
            AttendanceUseCases().create(AttendanceEntity(
                qty_of_terminals=1,
                work_center=work_center,
                attendance_date=self._get_date_days_ago(int(days_limit) / 2),
            ))


    def _register_fake_expeditions_in(self, work_center: WorkCentersEntity, qty_of_expeditions: int = 1, qty_of_terminals_per_expedition: int = 100):
        while len(ExpeditionsUseCases().get_all()) < qty_of_expeditions:
            ExpeditionsUseCases().create(ExpeditionsEntity(
                qty_of_terminals=qty_of_terminals_per_expedition,
                work_center=work_center
            ))

