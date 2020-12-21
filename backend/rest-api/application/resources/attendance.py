import falcon
from falcon import Request, Response
from use_cases.work_centers import WorkCentersUseCases
from use_cases.attendance import AttendanceUseCases
from application.hooks import verify_if_is_a_valid_work_center_to_register
from business.domain.entities import AttendanceEntity
from application.utils.json import serialize, prepare_list_to_json
from application.resources.work_centers import WorkCenterResource
from business.messages import AttendanceOperationsRejectionMessages
from utils.exceptions import UseCaseException, ApplicationLayerException
from utils.parses import parse_date_time_str_to_datetime
from data.data_source import DBDataSource
import datetime
import json


class AttendenceResourceMixin():
    _data_source = None
    _resource_use_cases = None
    _work_centers_use_case = None

    def __init__(self, data_source: DBDataSource):
        self._data_source = data_source
        self._resource_use_cases = AttendanceUseCases(self._data_source)
        self._work_centers_use_case = WorkCentersUseCases(self._data_source)


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
        attendance = {}

        try:
            attendance_data = req.media
            work_center_of_attendance = None
            work_center_id = attendance_data.get('work_center_id')

            if work_center_id != None:
                work_center_of_attendance = self._work_centers_use_case.find(work_center_id)
            
            if work_center_of_attendance == None:
                falcon.HTTPError(
                    "Error", AttendanceOperationsRejectionMessages.WORK_CENTER_IS_REQUIRED)

            attendance = AttendanceEntity()
            attendance.fill(
                qty_of_terminals=attendance_data.get('qty_of_terminals'),
                work_center=work_center_of_attendance,
                attendance_date=self._try_to_convert_date_json_to_datetime(
                    attendance_data.get('attendance_date'))
            )

            attendance = self._resource_use_cases.create(attendance)
            self._work_centers_use_case.update_calculated_values(work_center_of_attendance)
            attendance_updated = self._resource_use_cases.find(attendance.id)

        except UseCaseException as ex:
            raise falcon.HTTPBadRequest(falcon.HTTP_400, str(ex))
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))

        resp.status = falcon.HTTP_CREATED
        resp.body = falcon.media.JSONHandler().serialize(
            attendance_updated.to_dict(), falcon.MEDIA_JSON)

    def on_get(self, req: Request, resp: Response):
        try:
            resp.media = prepare_list_to_json(self._resource_use_cases.get_all())
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK
        except Exception as ex:
            raise falcon.HTTPError(str(ex))


class AttendanceResource(AttendenceResourceMixin):
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
                was_canceled=req.media.get('was_canceled'),
                attendance_date=self._try_to_convert_date_json_to_datetime(
                    req.media.get('attendance_date'))
            )

            attendance = self._resource_use_cases.update(found_entity)
            self._work_centers_use_case.update_calculated_values(attendance.work_center)
            attendance_updated = self._resource_use_cases.find(attendance.id)

            resp.media = attendance_updated.to_dict()
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_OK
        except UseCaseException as ex:
            raise falcon.HTTPBadRequest(falcon.HTTP_400, str(ex))
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))
        
        
        
