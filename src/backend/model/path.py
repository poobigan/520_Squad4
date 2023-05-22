class Path:
    """
       This class contains all the getter an setter methods needed for all the path related data
    """

    def __init__(self):
        self.path = []
        self.algo = "Empty"
        self.path_length = 0.0
        self.start_point = None, None
        self.end_point = None, None
        self.total_ele_gain = 0
        self.total_ele_drop = 0
        

    def set_algo(self, algo):
        """
        Sets the algorithm name when changed by the user.

        Args:
            algo: The new algorithm name.

        Returns:
            None
        """
        self.algo = algo

    def set_total_ele_gain(self, total_ele_gain):
        """
        Sets the total gain calculated using any algorithm.

        Args:
            total_ele_gain: The total gain value.

        Returns:
            None
        """
        self.total_ele_gain = total_ele_gain

    def set_total_ele_drop(self, total_ele_drop):
        """
        Sets the total drop calculated using any algorithm.

        Args:
            total_ele_drop: The total drop value.

        Returns:
            None
        """
        self.total_ele_drop = total_ele_drop

    def set_path(self, path):
        """
        Sets the path calculated using any algorithm.

        Args:
            path: The path as a list of nodes.

        Returns:
            None
        """
        self.path = path

    def set_path_length(self, path_length):
        """
        Sets the path length calculated using any algorithm.

        Args:
            path_length: The total path length value.

        Returns:
            None
        """
        self.path_length = path_length

    def get_algo(self):
        """
        Retrieves the algorithm name.

        Returns:
            The algorithm name.
        """
        return self.algo

    def get_total_ele_gain(self):
        """
        Retrieves the total gain.

        Returns:
            The total gain value.
        """
        return self.total_ele_gain

    def get_total_ele_drop(self):
        """
        Retrieves the total drop.

        Returns:
            The total drop value.
        """
        return self.total_ele_drop

    def get_path(self):
        """
        Retrieves the path.

        Returns:
            The path as a list of nodes.
        """
        return self.path

    def get_path_length(self):
        """
        Retrieves the path length.

        Returns:
            The total path length value.
        """
        return self.path_length

    def set_start_point(self, start_point):
        """
        Sets the start point for the path.

        Args:
            start_point: The coordinates of the start point.

        Returns:
            None
        """
        self.start_point = start_point

    def get_start_point(self):
        """
        Retrieves the start point.

        Returns:
            The coordinates of the start point.
        """
        return self.start_point

    def set_end_point(self, end_point):
        """
        Sets the end point for the path.

        Args:
            end_point: The coordinates of the end point.

        Returns:
            None
        """
        self.end_point = end_point

    def get_end_point(self):
        """
        Retrieves the end point.

        Returns:
            The coordinates of the end point.
        """
        return self.end_point
