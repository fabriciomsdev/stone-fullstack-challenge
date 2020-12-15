import falcon
from falcon import Request, Response
from use_cases.work_centers import WorkCentersUseCases
import json
from service.hooks import verify_if_is_a_valid_work_center_to_register
from domain.entities import WorkCentersEntity
from service.utils.json import serialize

class WorkCentersResource(object):

    @falcon.before(verify_if_is_a_valid_work_center_to_register)
    def on_post(self, req: Request, resp: Response):
        result = {}

        try:
            result = WorkCentersUseCases().create(WorkCentersEntity(**req.media))
        except Exception as ex:
            return falcon.HTTPBadRequest("Bad Request", ex)

        resp.status = falcon.HTTP_CREATED
        resp.body = json.dumps(result.__dict__)

    def on_get(self, req: Request, resp: Response):
        
        try:
            resp.media = [serialize(entity) for entity in WorkCentersUseCases().get_all()]
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK
        except Exception as ex:
            return falcon.HTTPError(str(ex))
        
        
        
