import subprocess
import socket
import struct
import ctypes
import os
import inspect
import threading
import pickle

from sdl2 import *
from sdl2 import sdlgfx
import numpy as np

from util import triangle_patch, scaled_coords
from managers.manager_base import Panel

if __name__ != '__main__':
    from .backend_base import BackendBase
else:
    BackendBase = object


# This backend need horrible workarounds because OSX doesn't support the event polling method that the SDL uses
# to be called from places other than the main thread. To alleviate this, we create a separate process for the SDL
# interface.

SOCKET_LOCATION = "sdl_socket"


def send_packet(sck, bts):
    sck.send(struct.pack('!l', len(bts)) + bts)


def get_packet(sck):
    length_bytes = sck.recv(4)
    length, *_ = struct.unpack('!l', length_bytes)
    return sck.recv(length)


class SdlBackend(BackendBase):
    def __init__(self, manager):
        if os.path.exists(SOCKET_LOCATION):
            os.remove(SOCKET_LOCATION)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(SOCKET_LOCATION)

        # Unfortunately we can't use multiprocessing because that'll crash the SDL.
        subprocess.Popen(['python3', inspect.getfile(inspect.currentframe())])

        self.sock.listen(5)
        self.conn, addr = self.sock.accept()
        send_packet(self.conn, b''.join([p.to_bytes() for p in manager.get_layout()]))

    def show(self, colors):
        send_packet(self.conn, pickle.dumps(colors))

class SdlInterface:
    colors_event_type = SDL_RegisterEvents(1)
    colors_event = SDL_Event()
    colors_event.type = colors_event_type

    def __init__(self):
        self.exit = False
        self.colors = None
        self.panels = []
        self.width = 800
        self.height = 200

    def draw_colors(self, renderer):
        coords = np.array([triangle_patch([p.center_x, -p.center_y], p.orientation + 3*np.pi/2, 150).astype(int)
                           for p in self.panels])
        coords = scaled_coords(coords, self.width, self.height)

        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255)
        SDL_RenderClear(renderer)
        for triangle, color in zip(coords, self.colors):
            (x1, y1), (x2, y2), (x3, y3) = triangle.astype(np.int16)
            # x1, y1, x2, y2, x3, y3 = 640, 138, 800, 138, 720, 0
            r, g, b = (color * 255).astype(int)
            sdlgfx.filledTrigonRGBA(renderer, x1, y1, x2, y2, x3, y3, r, g, b, 255)
        SDL_RenderPresent(renderer)

    def run(self):
        threading.Thread(target=self.socket_thread).start()

        SDL_Init(SDL_INIT_VIDEO)
        window = SDL_CreateWindow("SDL Nanoleaf".encode(),
                                  SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                                  self.width, self.height, SDL_WINDOW_SHOWN | SDL_WINDOW_RESIZABLE)

        renderer = SDL_CreateRenderer(window, -1, 0)
        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255)
        SDL_RenderClear(renderer)
        SDL_RenderPresent(renderer)

        running = True
        event = SDL_Event()
        while running:
            while SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == SDL_QUIT:
                    running = False
                    break
                elif event.type == SdlInterface.colors_event_type:
                    self.draw_colors(renderer)
                elif event.type == SDL_WINDOWEVENT and event.window.event == SDL_WINDOWEVENT_RESIZED:
                    self.width = event.window.data1
                    self.height = event.window.data2
                    self.draw_colors(renderer)

        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(window)
        SDL_Quit()

        self.exit = True

    def socket_thread(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(SOCKET_LOCATION)

        p = get_packet(self.sock)
        self.panels = Panel.list_from_bytes(p)

        while not self.exit:
            self.colors = pickle.loads(get_packet(self.sock))
            SDL_PushEvent(SdlInterface.colors_event)


if __name__ == '__main__':
    SdlInterface().run()
