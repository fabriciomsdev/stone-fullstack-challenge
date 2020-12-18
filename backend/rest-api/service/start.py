import falcon
from service.resources.work_centers import WorkCentersResource, WorkCenterResource
from service.resources.expeditions import ExpeditionResource, ExpeditionsResource
from service.resources.attendance import AttendanceListResource, AttendanceResource
from data.data_source import DBDataSource
from falcon import media
import rapidjson
class ApplicationBuilder():
    application_layer = None

    def create_and_start_database(self):
        DBDataSource().connect_to_source('sqlite:///db.sqlite3')
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

        self.application_layer.req_options.media_handlers.update(extra_handlers)
        self.application_layer.resp_options.media_handlers.update(extra_handlers)

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

    def build(self):
        (self.create_and_start_database() 
            .create_application_layer_obj() 
            .define_custom_settings_for_application_layer() 
            .define_comunication_ways())

        return self.application_layer


app = ApplicationBuilder().build()
