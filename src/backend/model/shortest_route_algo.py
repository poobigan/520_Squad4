from src.backend.model.path import Path
from src.util.logger_util import get_logger_statements
from src.util.util import fetch_path_weight
import networkx as ntx
import osmnx as osx


LOGGER = get_logger_statements(__name__)
ELEVATION_GAIN = "elevation_gain"
SHORTEST = "Shortest Route"

class ShortestRouteAlgo:
    """
           This class is used to calculate the shortest route without considering the elevation gain
    """

    def __init__(self, graph):
        self.graph = graph
        self.source = None
        self.destination = None
        self.short_path = None
        self.short_distance = None
        
        

    def get_shortest_route(self, start, end):
        """
                This method is used to calculate the shortest path without considering any elevation gain like a normal map .
                Args:
                    source_point
                    destination_point

                Returns:
                    shortest_path route
        """

        graph = self.graph
        self.destination = osx.get_nearest_node(graph, end)
        self.source = osx.get_nearest_node(graph, start)
        # returns the shortest route from starting node to ending node based on distance
        self.short_path = ntx.shortest_path(graph, self.source, self.destination,
                                           'length')

        LOGGER.info("Shortest path computed")

        info_least_dist_route = Path()
        info_least_dist_route.set_end_point(self.destination)
        info_least_dist_route.set_start_point(self.source)
        info_least_dist_route.set_total_ele_gain(fetch_path_weight(self.graph, self.short_path, ELEVATION_GAIN))
        info_least_dist_route.set_total_ele_drop(0)
        info_least_dist_route.set_algo(SHORTEST)
        info_least_dist_route.set_path([[graph.nodes[route_node]['x'], graph.nodes[route_node]['y']]
                                     for route_node in self.short_path])
        total_distance = sum(osx.utils_graph.get_route_edge_attributes(graph, self.short_path, 'length'))
        info_least_dist_route.set_path_length(total_distance)
        return info_least_dist_route
