import falcon

class DistribuitionCentersResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = 'Wellcome to Stone Challenge APi'


app = falcon.API()
app.add_route("/hello", DistribuitionCentersResource())