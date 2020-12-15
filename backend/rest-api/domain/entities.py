
class WorkCentersEntity():
    id: int = None
    region: str = ''

    def __init__(self, region: str = None, id: int = None):
        self.id = id
        self.region = region