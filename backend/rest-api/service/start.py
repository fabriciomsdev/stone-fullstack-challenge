import falcon
from service.resources.work_centers import WorkCentersResource
from service.midleware import JSONTranslatorMiddleware
from domain.business_rules import WorkCenterBusinessValidationsRules
from data.data_source import DBDataSource

class ApplicationBuilder():
    application_layer = None

    def create_and_start_database(self):
        DBDataSource().build('sqlite:///db.sqlite3')
        return self

    def create_application_layer_obj(self):
        self.application_layer = falcon.API()
        return self

    def define_comunication_ways(self):
        self.application_layer.add_route("/work-centers", WorkCentersResource())
        return self

    def build(self):
        self.create_and_start_database() \
            .create_application_layer_obj() \
            .define_comunication_ways()

        return self.application_layer


app = ApplicationBuilder().build()