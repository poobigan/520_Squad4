from src.backend.model.path import Path
from src.util.logger_util import get_logger_statements
from src.util.Util import get_path_weight, astar_algorithm
import osmnx as osx
import networkx as ntx
import math

LOGGER = get_logger_statements(__name__)
DISTANCE_FROM_DESTINATION = 'dist_from_dest'
DIJKSTRA_ALGORITHM = "DijkstraAlgorithm"
ASTAR_ALGORITHM = "AStar"
ELEVATION_GAIN = "elevation_gain"


class DijkstraAlgo:
    """
       This class is used to calculate the shortest route using the Dijkstra's Algorithm and also considering the elevation gain.
    """
    def __init__(self, graph, shortest_dist, limiting_percent, elevation_mode, origin, target,
                 elevation_gain):
        self.graph = graph
        self.origin = origin
        self.target = target
        self.shortest_dist = shortest_dist
        self.elevation_path = None
        self.scale = 100
        self.elevation_mode = elevation_mode
        self.limiting_percent = limiting_percent
        self.elevation_gain = elevation_gain
        self.elevation_distance = None
    def get_shortest_route(self):
        """
                This method takes into consideration the weights and elevation gain into account and calculates the shortest route.
                Dijkstra is a special case of AStar with heuristic set to None.
                Returns:
                ShortestPath route
        """
        graph = self.graph
        # calculating the elevation gain and distance based on user selected min or max gain
        if self.elevation_mode == 'min':
            factor = 1
        else: 
            factor = -1
        
        self.elevation_path = ntx.shortest_path(graph, self.origin, self.target,
                                               'length')
        while self.scale < 15000:
            elevation_path = astar_algorithm(graph,
                                                source=self.origin,
                                                target=self.target,
                                                heuristic=None,
                                                weight=lambda x, y, d:
                                                math.exp(1 / self.scale * (d[0]['length'])) +
                                                math.exp(factor * d[0]['length'] * (
                                                        d[0]['grade'] + d[0]['grade_abs']) / 2)
                                                )

            elevation_distance = sum(osx.utils_graph.get_route_edge_attributes(graph, elevation_path, 'length'))
            elevation_gain_val = get_path_weight(self.graph, elevation_path, ELEVATION_GAIN)
            if (elevation_gain_val * factor) <= (self.elevation_gain * factor) and \
                elevation_distance <= (1 + self.limiting_percent) * self.shortest_dist:
                self.elevation_gain = elevation_gain_val
                self.elevation_path = elevation_path
                
            self.scale *= 5

        shortest_path = Path()
        shortest_path.set_total_ele_drop(0)
        shortest_path.set_algo(ASTAR_ALGORITHM)
        shortest_path.set_total_ele_gain(get_path_weight(self.graph, self.elevation_path, ELEVATION_GAIN))
        shortest_path.set_path([[graph.nodes[route_node]['x'], graph.nodes[route_node]['y']]
                                for route_node in self.elevation_path])

        shortest_path.set_path_length(
            sum(osx.utils_graph.get_route_edge_attributes(graph, self.elevation_path, 'length')))

        LOGGER.info("Shortest route output from the Dijkstra Algorithm")
        LOGGER.info(f"Shortest route: {shortest_path}")
        return shortest_path