import numpy as np
from matplotlib import cm

from .visualization_base import VisualizationBase


class PowerVisualization(VisualizationBase):
    def __init__(self, min_freq, max_freq, rate, cmap):
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.rate = rate
        self.n_panels = None
        self.maxima = None
        self.prev = None
        self.cmap = cm.get_cmap(cmap)

    def process_samples(self, samples, n_panels):
        if n_panels != self.n_panels:
            self.n_panels = n_panels
            self.maxima = np.ones(n_panels)
            self.prev = np.zeros(n_panels)

        arr = np.frombuffer(samples, dtype=np.int16)
        freqs = np.fft.rfftfreq(len(arr), 1 / self.rate)
        cutoff_indices = np.searchsorted(freqs, np.logspace(np.log10(self.min_freq), np.log10(self.max_freq),
                                                            n_panels + 1))
        ft = np.fft.rfft(arr)
        binned = np.array([np.abs(np.average(ft[i:j])) for (i, j) in zip(cutoff_indices, cutoff_indices[1:])]) ** 2

        self.maxima = np.maximum(self.maxima, binned) * 0.95
        # print(f"Max: {self.maxima}")
        self.prev = 0.3 * np.clip(binned / self.maxima * (1/0.95), 0, 1) + 0.7 * self.prev
        # print(f"Prev: {self.prev}")
        #self.prev = np.clip(binned / 1e9, 0, 1)

        return self.cmap(self.prev)[:, :3]
