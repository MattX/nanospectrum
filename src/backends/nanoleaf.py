from backends.backend_base import BackendBase


class NanoleafBackend(BackendBase):
    def __init__(self, manager):
        self.manager = manager

    def show(self, colors):
        self.manager.put_colors(colors)
