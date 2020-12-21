import falcon
from falcon import Request, Response
from use_cases.work_centers import WorkCentersUseCases
from use_cases.expeditions import ExpeditionsUseCases
from application.hooks import verify_if_is_a_valid_work_center_to_register
from business.domain.entities import ExpeditionsEntity
from application.utils.json import serialize, prepare_list_to_json
from application.resources.work_centers import WorkCenterResource
from business.messages import ExpeditionOperationsRejectionMessages
from utils.exceptions import UseCaseException
from data.data_source import DBDataSource
import json

class ExpeditionsResource(object):
    _data_source = None
    _resource_use_cases = None
    _work_centers_use_case = None

    def __init__(self, data_source: DBDataSource):
        self._data_source = data_source
        self._resource_use_cases = ExpeditionsUseCases(self._data_source)
        self._work_centers_use_case = WorkCentersUseCases(self._data_source)

    def on_post(self, req: Request, resp: Response):
        result = {}
        try:
            expedition_data = req.media
            destiny_of_expedition = None
            work_center_id = expedition_data.get('work_center_id')

            if work_center_id != None:
                destiny_of_expedition = self._work_centers_use_case.find(
                    work_center_id)
            
            if destiny_of_expedition == None:
                falcon.HTTPError(
                    "Error", ExpeditionOperationsRejectionMessages.WORK_CENTER_IS_REQUIRED)

            expedition = ExpeditionsEntity()
            expedition.fill(
                qty_of_terminals=expedition_data.get('qty_of_terminals'),
                work_center=destiny_of_expedition,
                auto_predict_qty_needed=expedition_data.get('auto_predict_qty_needed'),
            )

            result = self._resource_use_cases.create(expedition)
        except UseCaseException as ex:
            raise falcon.HTTPBadRequest(falcon.HTTP_400, str(ex))
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))

        resp.status = falcon.HTTP_CREATED
        resp.body = falcon.media.JSONHandler().serialize(
            result.to_dict(), falcon.MEDIA_JSON)

    def on_get(self, req: Request, resp: Response):
        try:
            resp.media = prepare_list_to_json(self._resource_use_cases.get_all())
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK
        except Exception as ex:
            raise falcon.HTTPError(str(ex))

class ExpeditionResource(object):
    _data_source = None
    _resource_use_cases = None

    def __init__(self, data_source: DBDataSource):
        self._data_source = data_source
        self._resource_use_cases = ExpeditionsUseCases(self._data_source)

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

        try:
            found_entity.fill(
                qty_of_terminals=req.media.get('qty_of_terminals'),
                was_canceled=req.media.get('was_canceled')
            )

            expedition_updated = self._resource_use_cases.update(found_entity)
            
            resp.media = expedition_updated.to_dict()
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK
        except UseCaseException as ex:
            raise falcon.HTTPBadRequest(falcon.HTTP_400, str(ex))
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))
        
        
        
