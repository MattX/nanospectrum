from abc import ABC, abstractmethod


class BackendBase(ABC):
    @abstractmethod
    def show(self, colors):
        """
        Displays a visualization.
        :param values: An array of colors to display
        """
