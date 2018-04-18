import threading
import queue
import time

from util import get_all_from_queue


class Engine:
    def __init__(self, recorder, manager, sample_rate, refresh_rate, visualization, backends):
        self.recorder = recorder
        self.manager = manager
        self.n_panels = self.manager.get_num_panels()
        self.refresh_rate = refresh_rate

        self.audio_queue = queue.Queue()
        self.visualization = visualization
        self.visualization_queue = queue.Queue(maxsize=1)
        self.backends = backends
        self.backend_queues = [queue.Queue(maxsize=5) for _ in self.backends]
        self.recorder_thread = threading.Thread(target=self.recorder.record, args=(self.audio_queue, sample_rate))
        self.visualization_thread = threading.Thread(target=self.poll_to_visualization)
        self.multiplexer_thread = threading.Thread(target=self.poll_to_backends)

        self.backend_threads = [threading.Thread(target=self.run_backend, args=(bq, backend))
                                for (bq, backend) in zip(self.backend_queues, self.backends)]

    def start(self):
        self.recorder_thread.start()
        self.visualization_thread.start()
        self.multiplexer_thread.start()
        for bt in self.backend_threads:
            bt.start()

    def poll_to_visualization(self):
        while True:
            data = b''.join(get_all_from_queue(self.audio_queue))
            colors = self.visualization.process_samples(data, self.n_panels)
            self.visualization_queue.put(colors)

    def poll_to_backends(self):
        while True:
            colors = self.visualization_queue.get()
            for bq, backend in zip(self.backend_queues, self.backends):
                try:
                    bq.put_nowait(colors)
                except queue.Full:
                    print(f"Backend {backend} is running late!")
            time.sleep(self.refresh_rate)

    @staticmethod
    def run_backend(q, backend):
        while True:
            backend.show(q.get())
