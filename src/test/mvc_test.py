import unittest

from src.driver import *

class MVCTestSuite(unittest.TestCase):
    """
    This class contains unittest cases to check the working of the model view controller architecture.
    """

    def test_dijkstra_controller(self):
        """
        This test case checks if the dijkstra controller makes the required changes to the model.
        Returns:

        """
        destination = (42.4068893,-72.5408023)
        start = (42.3493904,-72.5325562)
        path_limit = 50
        elevation_strategy = 'min'
        controller = DijkstraController()
        model = Model()
        view = View()
        model.set_observer_obj(view)
        controller.set_model(model)
        controller.set_origin(start)
        controller.set_destination(destination)
        controller.set_limiting_percent(path_limit)
        controller.set_elevation_mode(elevation_strategy)
        controller.modify_model()
        assert model.algo == DijkstraAlgo

    def test_astar_controller(self):
        """
        This method checks if the astar controller makes the required changes to the model.
        Returns:

        """
        destination = (42.4068893,-72.5408023)
        start = (42.3493904,-72.5325562)
        path_limit = 50
        elevation_strategy = 'min'
        controller = AstarController()
        model = Model()
        view = View()
        model.set_observer_obj(view)
        controller.set_model(model)
        controller.set_origin(start)
        controller.set_destination(destination)
        controller.set_limiting_percent(path_limit)
        controller.set_elevation_mode(elevation_strategy)
        controller.modify_model()
        assert model.algo == AstarAlgo


if __name__ == '__main__':
    unittest.main()
