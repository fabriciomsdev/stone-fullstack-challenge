import environ

import falcon
from falcon import media
import rapidjson

from service.resources.work_centers import WorkCentersResource, WorkCenterResource
from service.resources.expeditions import ExpeditionResource, ExpeditionsResource
from service.resources.attendance import AttendanceListResource, AttendanceResource
from data.data_source import DBDataSource


class ApplicationBuilder():
    application_layer = None
    _env = None
    _is_in_tests = False
    _db_connection_for_tests = 'sqlite:///db.sqlite3'

    def create_and_start_database(self):
        if self._is_in_tests is True:
            DBDataSource().connect_to_source(self._db_connection_for_tests)
        else:
            DBDataSource().connect_to_source(self._env('DATABASE_CONNECTION_STR'))
        return self

    def create_application_layer_obj(self):
        self.application_layer = falcon.API(media_type='application/json')
        return self

    def define_custom_settings_for_application_layer(self):
        json_handler = media.JSONHandler(
            dumps=rapidjson.dumps,
            loads=rapidjson.loads,
        )
        extra_handlers = {
            'application/json': json_handler,
        }

        self.application_layer.req_options.media_handlers.update(
            extra_handlers)
        self.application_layer.resp_options.media_handlers.update(
            extra_handlers)

        return self

    def define_comunication_ways(self):
        self.application_layer.add_route(
            "/work-centers", WorkCentersResource())
        self.application_layer.add_route(
            "/work-centers/{primary_key}", WorkCenterResource())

        self.application_layer.add_route(
            "/expeditions", ExpeditionsResource())
        self.application_layer.add_route(
            "/expeditions/{primary_key}", ExpeditionResource())

        self.application_layer.add_route(
            "/attendance", AttendanceListResource())
        self.application_layer.add_route(
            "/attendance/{primary_key}", AttendanceResource())

        return self

    def define_env_vars(self):
        self._env = environ.Env(
            DEBUG=(bool, False),
            DATABASE_CONNECTION_STR=(
                str, self._db_connection_for_tests)
        )
        return self

    def read_env_archive(self):
        environ.Env.read_env()
        return self

    def build(self, for_tests = False):
        self._is_in_tests = for_tests

        (self.define_env_vars()
            .read_env_archive()
            .create_and_start_database()
            .create_application_layer_obj()
            .define_custom_settings_for_application_layer()
            .define_comunication_ways())

        return self.application_layer
