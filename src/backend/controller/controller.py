from abc import ABC, abstractmethod
"""
    This class serves as an abstract controller and contains methods that need to be implemented by its subclasses.
"""
class Controller(ABC):

    def __init__(self):
        self.model = None
        self.elevation_mode = None
        self.observer_obj = None
        
    @abstractmethod
    def set_model(self, model):
        pass

    @abstractmethod
    def modify_model(self):
        pass

    @abstractmethod
    def set_elevation_mode(self, elevation_mode):
        pass