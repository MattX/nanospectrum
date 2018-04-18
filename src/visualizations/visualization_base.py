from abc import ABC, abstractmethod


class VisualizationBase(ABC):
    @abstractmethod
    def process_samples(self, samples, n_panels):
        """
        Returns
        :param samples: A numpy array (of dtype int16) representing the samples collected since the last time this
        method was called.
        :param n_panels: The number of panels
        :return: An `n_panels` by 3 numpy array representing the color to set each panel to.
        """
        pass
