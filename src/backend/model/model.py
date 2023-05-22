from src.backend.model.MapNetworkGenerator import NetworkGenerator
from src.backend.model.LeastDistanceRoute import ShortestPathAlgorithm
from src.util.Util import get_address
from src.util.logger_util import get_logger_statements

LOGGER_STATEMENTS = get_logger_statements(__name__)


class Model:
    """
        This class initializes model parameters like the graph, algorithm, route choice among others. Methods are defined to set the
        observer, algorithm, algorithm object, print route information and generate routes.
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

    def get_map_api_key(self):
        return self.map_api_key

    def set_mapbox_api(self, api_key):
        self.map_api_key = api_key

    def set_observer_obj(self, observer_obj):
        self.observer_obj = observer_obj

    def set_algo(self, algo):
        self.algo = algo

    def get_obj_algo(self):
        return self.obj_algo

    def set_obj_algo(self):
        self.obj_algo = self.algo(self.graph,
                                    self.elevation_mode,
                                    self.percentage_limit,
                                    self.info_least_dist_route.get_start_node(),
                                    self.info_least_dist_route.get_end_node(),
                                    self.info_least_dist_route.get_distance(),
                                    self.info_least_dist_route.get_total_gain())

    def set_obj_least_dist_route(self, origin_coordinates, destination_coordinates):
        self.graph = NetworkGenerator().generate_graph_to_destination(destination_coordinates)
        self.obj_least_dist_route = ShortestPathAlgorithm(self.graph)
        self.info_least_dist_route = self.obj_least_dist_route.get_shortest_route(origin_coordinates, destination_coordinates)

    def print_route_details(self, route):
        LOGGER_STATEMENTS.info("#")
        LOGGER_STATEMENTS.info(f"Algorithm Strategy: {route.get_algo()}")
        LOGGER_STATEMENTS.info(f"Total Distance: {str(route.get_distance())}")
        LOGGER_STATEMENTS.info(f"Elevation Gain: {str(route.get_total_gain())}")
        LOGGER_STATEMENTS.info("#")

    def generate_routes(self, origin, destination, percentage_limit, elevation_mode):
        self.set_obj_least_dist_route(origin, destination)
        self.print_route_details(self.info_least_dist_route)
        if percentage_limit == 0:
            self.observer_obj.update_notifier(get_address(origin),
                                                get_address(destination),
                                                self.info_least_dist_route,
                                                self.info_least_dist_route)
            return

        self.percentage_limit = percentage_limit / 100.0
        self.elevation_mode = elevation_mode

        self.set_obj_algo()
        LOGGER_STATEMENTS.info(f"Algorithm information: {self.get_obj_algo()}")
        self.info_elevation_route = self.get_obj_algo().get_shortest_route()

        self.print_route_details(self.info_elevation_route)
        self.observer_obj.update_notifier(get_address(origin),
                                            get_address(destination),
                                            self.info_least_dist_route,
                                            self.info_elevation_route)
