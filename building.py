from ursina import *

WAREHOUSE_COST = 450000

class Warehouse(Entity):
    def __init__(self, pos):
        super().__init__()
        self.model='resources/city1.obj'
        self.texture = 'resources/bld1.png'
        self.scale = .04
        self.position = pos
        self.effect = 10
        self.name = "Warehouse"
        self.maintenance = 150000
        self.owner = None
        self.on_click = self.showWarehouseInfo

    def showWarehouseInfo(self):
        pass


