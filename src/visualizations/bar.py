import numpy as np
from matplotlib import cm

from .visualization_base import VisualizationBase


class BarVisualization(VisualizationBase):
    def __init__(self, manager):
        self.cmap = cm.get_cmap('jet')
        self.fonts = []

    def process_samples(self, samples, n_panels):
        return np.array([[0.1, 0.1, 0.1]] * n_panels)
