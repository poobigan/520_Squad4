import json

import googlemaps
from flask import Flask, request, render_template
from src.backend.controller.astar_controller import *
from src.backend.controller.dijkstra_controller import *
from src.backend.model.model import *
from src.view.View import View

GMAP_API_KEY = 'AIzaSyBB07RMmFyfyUYwXUbzQDduEmBiWyBUzlc'
gmaps = googlemaps.Client(key=GMAP_API_KEY)
access_key = 'pk.eyJ1IjoicG9vYmlnYW4iLCJhIjoiY2xocG14eGpoMDhiNTNubzV6b2JjYmNsdyJ9.oUoNfI-5XztqJjeEUNF8yw'
static_url_path = ''
static_folder = "./view/static"
template_folder = "./view/templates"
app = Flask(__name__, static_folder=static_folder, template_folder=template_folder, static_url_path=static_url_path)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)


ASTAR_ALGO = 'AstarAlgorithm'
DIJKSTRA_ALGO = 'DijkstraAlgorithm'
ORIGIN_COORDINATES = 'source_coordinates'
DESTINATION_COORDINATES = 'destination_coordinates'
START_ADDRESS = 'manual_source_address'
DESTINATION_ADDRESS = 'manual_destination_address'

@app.route('/view')
def client():
    """
        This method is used to render the UI
        Returns:
            Rendered template for UI
    """
    return render_template('view.html', ACCESS_KEY=access_key)


def get_controller_obj(algo):
    """
        This method is used to assign a controller object to the model based on algorithm chosen

        Args:
            algo: The algorithm selected by the user in the UI (AstarAlgorithm or DijkstraAlgorithm)

        Returns:
            Controller object
    """
    LOGGER.info(f"algo from driver: {algo}")
    if algo == "AstarAlgo":
        controller_object = AstarController()
    else:
        controller_object = DijkstraController()
    return controller_object


@app.route('/path_via_pointers', methods=['POST'])
def get_route():
    """
        This method assigns the values from the user selection on the map to parameters,
        initiates the controller and model, gets the best route details that will be shown finally

        Returns:
            Gets the view that is rendered to the user
    """
    json_out = request.get_json(force=True)
    LOGGER.info(f"Request: {json_out}")

    algorithm = json_out['algo']
    elevation_mode = json_out['minimum_maximum']
    path_limit = float(json_out['limiting_percent'])
    origin_coordinates = json.loads(json_out['source_coordinates'])
    destination_coordinates = json.loads(json_out['destination_coordinates'])
    start_point = (origin_coordinates['lat'], origin_coordinates['lng'])
    destination_point = (destination_coordinates['lat'], destination_coordinates['lng'])

    data_model = Model()
    view = View()
    data_model.set_observer_obj(view)
    controller = get_controller_obj(algorithm)
    controller.set_limiting_percent(path_limit)
    controller.set_elevation_mode(elevation_mode)
    controller.set_model(data_model)
    controller.set_origin(start_point)
    controller.set_destination(destination_point)
    controller.modify_model()
    return view.fetch_json_output()


def get_coordinates_from_address(address):
    """
        This method is used to get the geocoordinates from the address given

        Args:
            address: The user entered address

        Returns:
            The latitude and longitude values of the user entered address(address)
    """
    geocode = gmaps.geocode(address)
    return geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng']


@app.route('/path_via_address', methods=['POST'])
def get_routes():
    """
        This method takes the addresses from the user input fields(source and destination) in the UI 
        and assigns values to parameters, instantiates the controller and model objects and 
        gets the best route to be displayed with details and attributes

        Returns:
            Gets the view rendered in the UI
    """
    json_out = request.get_json(force=True)
    LOGGER.info(f"Request: {json_out}")
    start_address = json_out[START_ADDRESS]
    end_address = json_out[DESTINATION_ADDRESS]

    geocode = gmaps.geocode(start_address)
    print("Geocode", geocode)
    start_point = geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng']
    geocode = gmaps.geocode(end_address)
    destination_point = geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng']

    LOGGER.info(f"Origin point: {start_point}")
    LOGGER.info(f"Destination: {destination_point}")

    algorithm = json_out['algo']
    path_limit = float(json_out['limiting_percent'])
    elevation_strategy = json_out['minimum_maximum']

    data_model = Model()
    view = View()
    data_model.set_observer_obj(view)

    controller = get_controller_obj(algorithm)
    controller.set_model(data_model)
    controller.set_limiting_percent(path_limit)
    controller.set_elevation_mode(elevation_strategy)
    controller.set_origin(start_point)
    controller.set_destination(destination_point)
    controller.modify_model()
    output = view.fetch_json_output()

    return output
