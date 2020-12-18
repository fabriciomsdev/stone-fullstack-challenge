import falcon
from falcon import Request, Response
from use_cases.work_centers import WorkCentersUseCases
from use_cases.attendance import AttendanceUseCases
from service.hooks import verify_if_is_a_valid_work_center_to_register
from domain.entities import AttendanceEntity
from service.utils.json import serialize, serialize_list
from service.resources.work_centers import WorkCenterResource
from domain.business_messages import AttendanceOperationsRejectionMessages
from utils.exceptions import UseCaseException, ApplicationLayerException
import json
from utils.parses import parse_date_time_str_to_datetime
import datetime

class AttendenceResourceMixin():
    def _try_to_convert_date_json_to_datetime(self, date_in_json) -> datetime:
        if date_in_json is None:
            return None

        try:
            return parse_date_time_str_to_datetime(date_in_json)
        except Exception as ex:
            raise ApplicationLayerException(
                AttendanceOperationsRejectionMessages.ATTENDANCE_DATE_IS_INVALID)


class AttendanceListResource(AttendenceResourceMixin):

    def on_post(self, req: Request, resp: Response):
        result = {}

        try:
            attendance_data = req.media
            destiny_of_attendance = None
            work_center_id = attendance_data.get('work_center_id')

            if work_center_id != None:
                destiny_of_attendance = WorkCentersUseCases().find(work_center_id)
            
            if destiny_of_attendance == None:
                falcon.HTTPError(
                    "Error", AttendanceOperationsRejectionMessages.WORK_CENTER_IS_REQUIRED)

            attendance = AttendanceEntity()
            attendance.fill(
                qty_of_terminals=attendance_data.get('qty_of_terminals'),
                work_center=destiny_of_attendance,
                attendance_date=self._try_to_convert_date_json_to_datetime(
                    attendance_data.get('attendance_date'))
            )

            result = AttendanceUseCases().create(attendance)
        except UseCaseException as ex:
            raise falcon.HTTPBadRequest(falcon.HTTP_400, str(ex))
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))

        resp.status = falcon.HTTP_CREATED
        resp.body = falcon.media.JSONHandler().serialize(
            result.to_dict(), falcon.MEDIA_JSON)

    def on_get(self, req: Request, resp: Response):
        try:
            resp.media = serialize_list(AttendanceUseCases().get_all())
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK
        except Exception as ex:
            raise falcon.HTTPError(str(ex))


class AttendanceResource(AttendenceResourceMixin):
    def on_get(self, req: Request, resp: Response, primary_key: int):
        found_entity = AttendanceUseCases().find(primary_key=primary_key)

        if found_entity == None:
            raise falcon.HTTPNotFound()

        resp.media = serialize(found_entity.to_dict())
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_OK

    def on_delete(self, req: Request, resp: Response, primary_key: int):
        found_entity = AttendanceUseCases().find(primary_key=primary_key)

        if found_entity == None:
            raise falcon.HTTPNotFound()

        try:
            resp.body = json.dumps(AttendanceUseCases().delete(found_entity))
            resp.status = falcon.HTTP_OK
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))

    def on_put(self, req: Request, resp: Response, primary_key: int):
        found_entity = AttendanceUseCases().find(primary_key=primary_key)
        if found_entity == None:
            raise falcon.HTTPNotFound()

        try:
            found_entity.fill(
                qty_of_terminals=req.media.get('qty_of_terminals'),
                was_canceled=req.media.get('was_canceled'),
                attendance_date=self._try_to_convert_date_json_to_datetime(
                    req.media.get('attendance_date'))
            )

            attendance_updated = AttendanceUseCases().update(found_entity)
            
            resp.body = serialize(attendance_updated.to_dict())
            resp.status = falcon.HTTP_OK
        except UseCaseException as ex:
            raise falcon.HTTPBadRequest(falcon.HTTP_400, str(ex))
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))
        
        
        
