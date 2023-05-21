from src.backend.model.astar_algo import *
from src.backend.controller.controller import *
"""
   This controller implements the Astar Algorithm, which calculates the shortest path between
    a source and destination, while considering the elevation.
"""
class AstarController(Controller):

    def __init__(self):
        super().__init__()
        self.source = None
        self.destination = None
        self.model = None
        self.limiting_percent = None
        self.elevation_mode = None
        self.observer_obj = None

    def set_origin(self, source):
        self.source = source

    def set_destination(self, destination):
        self.destination = destination

    def set_model(self, model):
        self.model = model

    def set_elevation_mode(self, elevation_mode):
        self.elevation_mode = elevation_mode
    
    def set_limiting_percent(self, limiting_percent):
        self.limiting_percent = limiting_percent

    def modify_model(self):
        self.model.set_algo(AstarAlgo)
        self.model.generate_routes(self.source, self.destination, self.limiting_percent, self.elevation_mode)