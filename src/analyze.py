import queue

import numpy as np


MIN_FREQ = 100
MAX_FREQ = 1000


def pull_analyze(q_in, q_out, n_panels, rate):
    while True:
        # Get as much of the queue as possible
        data = q_in.get()
        while True:
            try:
                data += q_in.get_nowait()
            except queue.Empty:
                break

        arr = np.frombuffer(data, dtype=np.int16)
        freqs = np.fft.rfftfreq(len(arr), 1 / rate)
        cutoff_indices = np.searchsorted(freqs, np.logspace(np.log10(MIN_FREQ), np.log10(MAX_FREQ), n_panels + 1))
        #print(f"CO: {cutoff_indices}")
        ft = np.fft.rfft(arr)
        binned = np.array([np.abs(np.average(ft[i:j])) for (i, j) in zip(cutoff_indices, cutoff_indices[1:])]) ** 2
        #print(f"Binned: {binned}")
        q_out.put(binned)
