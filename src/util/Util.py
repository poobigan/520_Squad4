from geopy.geocoders import Nominatim
import networkx as nx
from heapq import heappush, heappop
from itertools import count
from networkx.algorithms.shortest_paths.weighted import _weight_function

NORMAL = "normal"
ELEVATION_GAIN = "elevation_gain"

WEIGHT = 'weight'
ELEVATION = 'elevation'
LENGTH = 'length'

PROPERTIES = "properties"
GEOMETRY = "geometry"
TYPE = "type"
COORDINATES = "coordinates"
FEATURE = "Feature"
LINESTRING = "LineString"


def astar_algorithm(graph, min_cost_heuristics, weight, origin, destination):
    """
    This method is used to compute the least distance path between origin and destination using A-star algorithm

    Args:
        graph: NetworkX graph
        origin: Start node in the path
        destination: Final node in the path
        min_cost_heuristics: Gives an estimate of the minimum cost between any two nodes
        weight: Used to pass the edge weights

    Returns:
    All nodes in the least distance path between origin and destination
    """
    if not all(node in graph for node in [origin, destination]):
        print("Graph does not contain either origin or destination points")

    min_cost_heuristics = min_cost_heuristics if min_cost_heuristics is not None else lambda u, v: 0
        
    enqueue_dict = {}
    visited_nodes_dict = {}

    weight = _weight_function(graph, weight)
    counter = count()
    queue = [(0, next(counter), origin, 0, None)]
    while queue:
        _, __, current_node, distance, parent_node = heappop(queue)
        if current_node == destination:
            path = [current_node]
            node = parent_node
            while node is not None:
                path.append(node)
                node = visited_nodes_dict[node]
            path = path[::-1]
            return path
        
        if current_node not in visited_nodes_dict or visited_nodes_dict[current_node] is not None:
            visited_nodes_dict[current_node] = parent_node
            for neighbor, node_weight in graph[current_node].items():
                node_cost = distance + weight(current_node, neighbor, node_weight)
                if neighbor in enqueue_dict:
                    queue_cost, x = enqueue_dict[neighbor]
                    if queue_cost <= node_cost:
                        continue
                else:
                    x = min_cost_heuristics(neighbor, destination)
                enqueue_dict[neighbor] = node_cost, x
                node_to_push = (node_cost + x, next(counter), neighbor, node_cost, current_node)
                heappush(queue, node_to_push)

    raise nx.NetworkXNoPath(f"Cannot navigate from {origin} node to {destination} node")


def get_weight(graph, start_node, end_node, weight_type=NORMAL):
    """
    This method is used to get the edge weight based on path length or elevation gain

    Args:
        graph: graph object
        start_node: start node
        end_node: final node
        weight_type: normal/elevation (set to NORMAL by default)

    Returns:
        Edge weight of the edge connecting start and end nodes
    """
    if weight_type == NORMAL:
        try:
            return graph.edges[start_node, end_node, 0][LENGTH]
        except:
            return graph.edges[start_node, end_node][WEIGHT]
    elif weight_type == ELEVATION_GAIN:
        return max(0.0, graph.nodes[end_node][ELEVATION] - graph.nodes[start_node][ELEVATION])

def get_path_weight(graph, path, weight):
    """
    This method is used to get the path weight

    Args:
        graph: graph object
        path: route
        weight: weight

    Returns:
        total weight computed based on the path and weight params
    """
    total_weight = sum(get_weight(graph, path[i], path[i + 1], weight) for i in range(len(path) - 1))
    return total_weight


def get_address(geocoordinates):
    """
    This method is used to get the address from the coordinates

    Args:
        coordinates: latitude and longitude (geocoordinates)

    Returns:
        Address of the coordinates
    """
    return Nominatim(user_agent="myGeocoder").reverse(geocoordinates).address


def update_json_route(geocoordinates):
    """
    This method is used to update the json route with the coordinates

    Args:
        coordinates: geocoordinates

    Returns:
        Updated json route
    """
    json_route = {PROPERTIES: {}, GEOMETRY: {}, TYPE: FEATURE}
    json_route[GEOMETRY][COORDINATES] = geocoordinates
    json_route[GEOMETRY][TYPE] = LINESTRING
    return json_route