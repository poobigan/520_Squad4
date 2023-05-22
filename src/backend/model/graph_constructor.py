import os
import osmnx as osx
import pickle as pkl
from haversine import haversine, Unit
from src.util.logger_util import get_logger_statements

LOGGER = get_logger_statements(__name__)

DISTANCE_FROM_END_POINT = 'dist_from_dest'

class GraphConstructor:

    def __init__(self):
        self.graph = None
        self.gmap_api_key = "AIzaSyBB07RMmFyfyUYwXUbzQDduEmBiWyBUzlc"
        self.mid_point = (42.3559168,-72.5286912)
        self.map_location_offline = "../../openstreetmapoffline.p"

    def graph_from_filepath(self, filepath):
        try:
            self.graph = pkl.load(open(filepath, "rb"))
            LOGGER.info("Offline map load successful!")
            self.graph = osx.add_edge_grades(self.graph)
        except:
            if os.path.exists("../../openstreetmapoffline.p"):
                self.graph = pkl.load(open(self.map_location_offline, "rb"))
                LOGGER.info("Offline map load successful!")
                self.graph = osx.add_edge_grades(self.graph)
            else:
                LOGGER.info("Offline map download failed")
                self.download_map()

    def generate_graph_to_end_point(self, destination_node):
        # Updates the graph with distance from destination and returns it.
        print("Attempting to load Offline map....", self.map_location_offline)
        self.graph_from_filepath("src/openstreetmapoffline.p")

    # Graph is updated with distance from all nodes in graph to the end point
        final_node = self.graph.nodes[osx.get_nearest_node(self.graph, point=destination_node)]
        for node, data in self.graph.nodes(data=True):
            final_x = final_node['x']
            final_y = final_node['y']
            x_node = self.graph.nodes[node]['x']
            y_node = self.graph.nodes[node]['y']
            data[DISTANCE_FROM_END_POINT] = haversine((final_x, final_y), (x_node, y_node), unit=Unit.METERS)
        print(self.graph)
        return self.graph
    
    def download_map_from_osmnx(self):
        # This method gets the map from OSMNX and adds elevation attributes
        LOGGER.info("Successful map download!")
        self.graph = osx.graph_from_point(self.middle_point, dist=15000, network_type='walk')
        # Adding elevation attributes
        self.graph = osx.add_node_elevations(self.graph, api_key=self.gmap_api_key)

        # Saving graph with elevation attributes
        pkl.dump(self.graph, open(self.map_location_offline, "wb"))
        LOGGER.info("Graph save successful!")
