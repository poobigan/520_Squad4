class RouteAttributes:
    """
       This class has the getter-setter methods for all path related data
    """

    def __init__(self):
        self.path = []
        self.algo = "Empty"
        self.total_gain = 0
        self.total_drop = 0
        self.distance = 0.0
        self.start_node = None, None
        self.end_node = None, None

    def set_path(self, path):
        """
                This method sets the path for any algorithm chosen
                Args:
                    path:
                Returns:
                    None
        """
        self.path = path

    def get_path(self):
        """
                Getter method for fetching the path
                Returns:path

        """
        return self.path

    def set_algo(self, algo):
        """
                This method sets the algorithm according to user preference
                Args:
                    algo
                Returns:
                    None
        """
        self.algo = algo

    def get_algo(self):
        """
                Getter method for fetching algorithm
                Returns:algorithm name

        """
        return self.algo

    def set_total_gain(self, total_gain):
        """
                This method sets total_gain calculated for any algorithm chosen
                Args:
                    total_gain
                Returns:
                    None
        """
        self.total_gain = total_gain

    def get_total_gain(self):
        """
                Getter method for fetching the total gain
                Returns:total_gain

        """
        return self.total_gain

    def set_total_drop(self, total_drop):
        """
                This method sets total_drop calculated for any algorithm chosen
                Args:
                    total_drop
                Returns:
                    None
        """
        self.total_drop = total_drop

    def get_total_drop(self):
        """
                Getter method for fetching the total drop
                Returns:total_drop

        """
        return self.total_drop

    def set_distance(self, distance):
        """
                This method sets distance for the route calculated for the chosen algorithm
                Args:
                    distance
                Returns:
                    None
        """
        self.distance = distance

    def get_distance(self):
        """
                Getter method for fetching distance
                Returns:distance

        """
        return self.distance

    def set_start_node(self, start_node):
        """
                This method sets the route's start node
                Args:
                    start_node
                Returns:
                    None
        """
        self.start_node = start_node

    def get_start_node(self):
        """
                Getter method to fetch the route's start node
                Returns:
                    None
        """
        return self.start_node

    def set_end_node(self, end_node):
        """
                This method sets the route's end node
                Args:
                    end_node
                Returns:
                    None
        """
        self.end_node = end_node

    def get_end_node(self):
        """
                Getter method to fetch the route's end node
                Returns:
                    None
        """
        return self.end_node
