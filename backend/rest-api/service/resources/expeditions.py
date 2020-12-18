import falcon
from falcon import Request, Response
from use_cases.work_centers import WorkCentersUseCases
from use_cases.expeditions import ExpeditionsUseCases
from service.hooks import verify_if_is_a_valid_work_center_to_register
from domain.entities import ExpeditionsEntity
from service.utils.json import serialize, serialize_list
from service.resources.work_centers import WorkCenterResource
from domain.business_messages import ExpeditionOperationsRejectionMessages
from utils.exceptions import UseCaseException
import json

class ExpeditionsResource(object):

    def on_post(self, req: Request, resp: Response):
        result = {}

        try:
            expedition_data = req.media
            destiny_of_expedition = None
            work_center_id = expedition_data.get('work_center_id')

            if work_center_id != None:
                destiny_of_expedition = WorkCentersUseCases().find(work_center_id)
            
            if destiny_of_expedition == None:
                falcon.HTTPError(
                    "Error", ExpeditionOperationsRejectionMessages.WORK_CENTER_IS_REQUIRED)

            expedition = ExpeditionsEntity()
            expedition.fill(
                qty_of_items=expedition_data.get('qty_of_items'),
                work_center=destiny_of_expedition
            )

            result = ExpeditionsUseCases().create(expedition)
        except UseCaseException as ex:
            raise falcon.HTTPBadRequest(falcon.HTTP_400, str(ex))
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))

        resp.status = falcon.HTTP_CREATED
        resp.body = falcon.media.JSONHandler().serialize(
            result.to_dict(), falcon.MEDIA_JSON)

    def on_get(self, req: Request, resp: Response):
        try:
            resp.media = serialize_list(ExpeditionsUseCases().get_all())
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK
        except Exception as ex:
            raise falcon.HTTPError(str(ex))

class ExpeditionResource(object):
    def on_get(self, req: Request, resp: Response, primary_key: int):
        found_entity = ExpeditionsUseCases().find(primary_key=primary_key)

        if found_entity == None:
            raise falcon.HTTPNotFound()

        resp.media = serialize(found_entity.to_dict())
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_OK

    def on_delete(self, req: Request, resp: Response, primary_key: int):
        found_entity = ExpeditionsUseCases().find(primary_key=primary_key)

        if found_entity == None:
            raise falcon.HTTPNotFound()

        try:
            resp.body = json.dumps(ExpeditionsUseCases().delete(found_entity))
            resp.status = falcon.HTTP_OK
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))

    def on_put(self, req: Request, resp: Response, primary_key: int):
        found_entity = ExpeditionsUseCases().find(primary_key=primary_key)
        if found_entity == None:
            raise falcon.HTTPNotFound()

        try:
            found_entity.fill(
                qty_of_items=req.media.get('qty_of_items'),
                was_canceled=req.media.get('was_canceled')
            )

            expedition_updated = ExpeditionsUseCases().update(found_entity)
            
            resp.body = serialize(expedition_updated.to_dict())
            resp.status = falcon.HTTP_OK
        except UseCaseException as ex:
            raise falcon.HTTPBadRequest(falcon.HTTP_400, str(ex))
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))
        
        
        
