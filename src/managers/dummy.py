import numpy as np

from .manager_base import ManagerBase, Panel


class DummyManager(ManagerBase):
    def __init__(self, num_panels):
        self.num_panels = num_panels

    def get_num_panels(self):
        return self.num_panels

    def get_layout(self):
        return [Panel(i, 75*i, 43 * (1 - i % 2), np.pi/3 * (i % 2 + 1)) for i in range(self.num_panels)]

    def put_colors(self, colors):
        pass
