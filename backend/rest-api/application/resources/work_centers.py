import falcon
from falcon import Request, Response
from use_cases.work_centers import WorkCentersUseCases
import json
from application.hooks import verify_if_is_a_valid_work_center_to_register
from business.domain.entities import WorkCentersEntity
from application.utils.json import serialize, prepare_list_to_json
from data.data_source import DBDataSource

class WorkCentersResource(object):
    _data_source = None
    _resource_use_cases = None
    
    def __init__(self, data_source: DBDataSource):
        self._data_source = data_source
        self._resource_use_cases = WorkCentersUseCases(self._data_source)
        

    @falcon.before(verify_if_is_a_valid_work_center_to_register)
    def on_post(self, req: Request, resp: Response):
        result = {}

        try:
            result = self._resource_use_cases.create(WorkCentersEntity(**req.media))
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))

        resp.status = falcon.HTTP_CREATED
        resp.body = serialize(result)

    def on_get(self, req: Request, resp: Response):
        try:
            resp.media = prepare_list_to_json(self._resource_use_cases.get_all())
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK
        except Exception as ex:
            raise falcon.HTTPError(str(ex))

class WorkCenterResource(object):
    _data_source = None
    _resource_use_cases = None

    def __init__(self, data_source: DBDataSource):
        self._data_source = data_source
        self._resource_use_cases = WorkCentersUseCases(self._data_source)

    def on_get(self, req: Request, resp: Response, primary_key: int):
        found_entity = self._resource_use_cases.find(primary_key=primary_key)

        if found_entity == None:
            raise falcon.HTTPNotFound()

        resp.media = found_entity.to_dict()
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_OK

    def on_delete(self, req: Request, resp: Response, primary_key: int):
        found_entity = self._resource_use_cases.find(primary_key=primary_key)

        if found_entity == None:
            raise falcon.HTTPNotFound()

        try:
            resp.body = json.dumps(self._resource_use_cases.delete(found_entity))
            resp.status = falcon.HTTP_OK
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))

    def on_put(self, req: Request, resp: Response, primary_key: int):
        found_entity = self._resource_use_cases.find(primary_key=primary_key)
        if found_entity == None:
            raise falcon.HTTPNotFound()

        found_entity.fill(region=req.media.get('region'))

        try:
            entity_updated = self._resource_use_cases.update(found_entity)
            resp.media = entity_updated.to_dict()
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))
        
        
        
