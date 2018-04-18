from abc import ABC, abstractmethod

from collections import namedtuple

Panel = namedtuple('Panel', ('id', 'center_x', 'center_y', 'orientation'))


class ManagerBase(ABC):
    """
    Todo: change layouts to remove the factor of 150
    """
    @abstractmethod
    def get_num_panels(self):
        pass

    @abstractmethod
    def get_layout(self):
        pass

    @abstractmethod
    def put_colors(self, colors):
        pass
