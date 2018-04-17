import numpy as np

from visualizations.visualization_base import VisualizationBase


class PowerVisualization(VisualizationBase):
    def __init__(self, min_freq, max_freq, rate):
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.rate = rate

    def process_samples(self, samples, n_panels):
        arr = np.frombuffer(samples, dtype=np.int16)
        freqs = np.fft.rfftfreq(len(arr), 1 / self.rate)
        cutoff_indices = np.searchsorted(freqs, np.logspace(np.log10(self.min_freq), np.log10(self.max_freq),
                                                            n_panels + 1))
        ft = np.fft.rfft(arr)
        binned = np.array([np.abs(np.average(ft[i:j])) for (i, j) in zip(cutoff_indices, cutoff_indices[1:])]) ** 2
        return binned
