import osmnx as ox
import networkx as nx
from src.util.Util import get_path_weight
from src.util.logger_util import get_logger_statements
from src.backend.model.RouteAttributes import RouteData

ELEVATION_GAIN = "elevation_gain"
LEAST_DISTANCE_PATH = "Shortest Path"
LOGGER_STATEMENTS = get_logger_statements(__name__)

class LeastDistanceRoute:
    """
           This class calculates the least distance route without any elevation gain
    """

    def __init__(self, graph):
        self.graph = graph
        self.source = None
        self.destination = None
        self.least_distance = None
        self.least_distance_path = None

    def get_shortest_route(self, start, end):
        """
                This method is used to calculate the shortest path without considering any elevation gain(like a normal map)
                Args:
                    start_point
                    end_point

                Returns:
                    shortest_path route
        """

        graph = self.graph
        self.source, self.destination = None, None

        self.source, _ = ox.get_nearest_node(graph, point=start, return_dist=True)
        self.destination, _ = ox.get_nearest_node(graph, point=end, return_dist=True)

        # returns the shortest route from starting node to ending node based on distance
        self.least_distance_path = nx.shortest_path(graph, source=self.source, target=self.destination,
                                           weight='length')

        LOGGER_STATEMENTS.info("Calculated the least distance route from origin to destination with elevation gain")

        info_least_dist_route = RouteData()
        info_least_dist_route.set_start_node(self.source)
        info_least_dist_route.set_end_node(self.destination)
        info_least_dist_route.set_algo(LEAST_DISTANCE_PATH)
        info_least_dist_route.set_total_gain(get_path_weight(self.graph, ELEVATION_GAIN, self.least_distance_path))
        info_least_dist_route.set_total_drop(0)
        info_least_dist_route.set_path([[graph.nodes[route_node]['x'], graph.nodes[route_node]['y']]
                                            for route_node in self.least_distance_path])
        total_distance = sum(ox.utils_graph.get_route_edge_attributes(graph, self.least_distance_path, 'length'))
        info_least_dist_route.set_distance(total_distance)
        return info_least_dist_route
