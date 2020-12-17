
class WorkCentersEntity():
    id: int = None
    region: str = ''

    def __init__(self, region: str = None, id: int = None):
        self.id = id
        self.fill(region)

    def fill(self, region: str = None):
        self.region = region


class ExpeditionEntity():
    id: int = None
    qty_of_items: int = 1

    def __init__(self, qty_of_items: int = 1, id: int = None):
        self.id = id
        self.fill(qty_of_items)

    def fill(self, qty_of_items: str = None):
        self.qty_of_items = qty_of_items

