import environ

import falcon
from falcon import media
import rapidjson

from application.resources.work_centers import WorkCentersResource, WorkCenterResource
from application.resources.expeditions import ExpeditionResource, ExpeditionsResource
from application.resources.attendance import AttendanceListResource, AttendanceResource
from data.data_source import DBDataSource


class WelcomeResource():
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = ('<h1> Welcome to Stone Api </h1>')


class ApplicationBuilder():

    application_layer = None
    _env = None
    _is_in_tests = False
    _db_connection_for_tests = 'sqlite:///db.sqliteTests'
    _data_source = DBDataSource()

    def create_and_start_database(self):
        if self._is_in_tests is True:
            self._data_source.connect_to_source(self._db_connection_for_tests)
        else:
            self._data_source.connect_to_source(self._env('DATABASE_CONNECTION_STR'))
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
            "/", WelcomeResource())

        self.application_layer.add_route(
            "/work-centers", WorkCentersResource(self._data_source))
        self.application_layer.add_route(
            "/work-centers/{primary_key}", WorkCenterResource(self._data_source))

        self.application_layer.add_route(
            "/expeditions", ExpeditionsResource(self._data_source))
        self.application_layer.add_route(
            "/expeditions/{primary_key}", ExpeditionResource(self._data_source))

        self.application_layer.add_route(
            "/attendance", AttendanceListResource(self._data_source))
        self.application_layer.add_route(
            "/attendance/{primary_key}", AttendanceResource(self._data_source))

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
