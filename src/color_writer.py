import queue
import time

import numpy as np


def pull_write_color(manager, q):
    prev = np.array([0] * manager.get_num_panels())
    max = np.array(prev)
    while True:
        # Get as much of the queue as possible
        data = q.get()
        while True:
            try:
                data = q.get_nowait()
            except queue.Empty:
                break

        max = np.maximum(max, data) * 0.95
        #print(f"Max: {max}")
        prev = 0.1 * np.clip(data / max * (1/0.95), 0, 1) + 0.9 * prev
        manager.put_values(prev)
        time.sleep(0.05)
