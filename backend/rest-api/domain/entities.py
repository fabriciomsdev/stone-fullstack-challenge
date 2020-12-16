
class WorkCentersEntity():
    id: int = None
    region: str = ''

    def __init__(self, region: str = None, id: int = None):
        self.id = id
        self.fill(region)

    def fill(self, region: str = None):
        self.region = region