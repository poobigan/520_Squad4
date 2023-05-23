from src.util.logger_util import get_logger_statements
from src.util.Util import get_address
from src.backend.model.shortest_route_algo import ShortestRouteAlgo
from src.backend.model.graph_constructor import GraphConstructor

LOGGER = get_logger_statements(__name__)


class Model:
    """
        This class initializes critical parameters such the graph,the algorithm,the path_limit  etc.It contains methods to register the
        observer_obj,set the algorithm,set the algorithm object,print the route information etc and also it notifies the observer_objs.
    """
    def __init__(self):
        self.map_api_key = None
        self.graph = None
        self.obj_least_dist_route = None
        self.info_least_dist_route = None
        self.obj_elevation_route = None
        self.info_elevation_route = None
        self.observer_obj = None
        self.algo = None
        self.obj_algo = None
        self.percentage_limit = None
        self.elevation_mode = None

    def get_mapbox_api(self):
        return self.map_api_key

    def set_mapbox_api(self, api_key):
        self.map_api_key = api_key

    def set_observer_obj(self, observer_obj):
        self.observer_obj = observer_obj

    def set_algo(self, algo):
        self.algo = algo

    def get_obj_algo(self):
        return self.obj_algo
    
    def set_obj_least_dist_route(self, origin, destination):
        self.graph = GraphConstructor().generate_graph_to_end_point(destination)
        self.obj_least_dist_route = ShortestRouteAlgo(self.graph)
        self.info_least_dist_route = self.obj_least_dist_route.get_shortest_route(origin, destination)

    def set_obj_algo(self):
        self.obj_algo = self.algo(self.graph,
                                            self.info_least_dist_route.get_path_length(),
                                            self.percentage_limit,
                                            self.elevation_mode,
                                            self.info_least_dist_route.get_start_point(),
                                            self.info_least_dist_route.get_end_point(),
                                            self.info_least_dist_route.get_total_ele_gain())

    def print_route_details(self, route):
        LOGGER.info("-")
        LOGGER.info(f"Chosen Algo: {route.get_algo()}")
        LOGGER.info(f"Total Distance: {str(route.get_path_length())}")
        LOGGER.info(f"Elevation Gain: {str(route.get_total_ele_gain())}")
        LOGGER.info("-")

    def generate_routes(self, origin, destination, percentage_limit, elevation_mode):
        self.set_obj_least_dist_route(origin, destination)
        self.print_route_details(self.info_least_dist_route)
        if percentage_limit == 0:
            self.observer_obj.update_notifier(self.info_least_dist_route,
                                          self.info_least_dist_route,
                                          get_address(origin),
                                          get_address(destination))
            return
        self.elevation_mode = elevation_mode
        self.percentage_limit = percentage_limit / 100.0
        

        self.set_obj_algo()
        LOGGER.info(f"Chosen algo: {self.get_obj_algo()}")
        self.info_elevation_route = self.get_obj_algo().get_shortest_route()

        self.print_route_details(self.info_elevation_route)

        self.observer_obj.update_notifier(self.info_least_dist_route,
                                      self.info_elevation_route,
                                      get_address(origin),
                                      get_address(destination))
