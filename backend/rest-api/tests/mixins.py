from data.repositories import WorkCentersRepository
from domain.entities import WorkCentersEntity
import json

class TestWithWorkCenterCreationMixin():
    _data_source = None

    def _create_a_work_center_by_data_layer(self):
        work_center_repository = WorkCentersRepository(self._data_source)
        work_center = WorkCentersEntity(region="SP - Osasco")

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