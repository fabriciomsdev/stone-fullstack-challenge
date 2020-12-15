import falcon
from use_cases.work_centers import CreateAWorkCentersUseCase
import json
from service.hooks import verify_if_is_a_valid_work_center_to_register
from domain.entities import WorkCentersEntity

class WorkCentersResource(object):

    @falcon.before(verify_if_is_a_valid_work_center_to_register)
    def on_post(self, req, resp):
        result = {}

        try:
            result = CreateAWorkCentersUseCase().execute(WorkCentersEntity(**req.media))
        except Exception as ex:
            falcon.HTTPBadRequest("Bad Request", ex)

        resp.status = falcon.HTTP_CREATED
        resp.body = json.dumps(result.__dict__)
        
