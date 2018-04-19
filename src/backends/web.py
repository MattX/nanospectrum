import io
import queue
import threading
import warnings

from PIL import Image, ImageDraw
import numpy as np
import flask

from util import triangle_patch
from .backend_base import BackendBase


class WebBackend(BackendBase):
    def __init__(self, manager, width=800, height=200):
        warnings.warn(UserWarning("WebBackend is experimental and suffers from poor performance"))
        self.n_panels = manager.get_num_panels()
        self.layout = manager.get_layout()
        self.png_queue = queue.Queue()
        self.width = width
        self.height = height
        threading.Thread(target=self.flask).start()

    def png(self, color_list):
        im = Image.new('RGB', (self.width, self.height), 'white')
        draw = ImageDraw.Draw(im)
        coords = np.array([triangle_patch([p.center_x, p.center_y], p.orientation + np.pi / 2, 150).astype(int)
                          .flatten().tolist() for p in self.layout])

        xlim = np.min(coords[:, ::2]), np.max(coords[:, ::2])
        ylim = np.min(coords[:, 1::2]), np.max(coords[:, 1::2])

        scale = min(self.width / (xlim[1] - xlim[0]), self.height / (ylim[1] - ylim[0]))
        # print(f"xlim {xlim}, ylim {ylim}, scale {scale}")

        # print(np.min(coords), xlim[0], ylim[0])
        coords[:, ::2] -= xlim[0]
        coords[:, 1::2] -= ylim[0]
        # print(np.min(coords))
        coords = (coords * scale)

        for c, color in zip(coords, color_list):
            draw.polygon(c.tolist(), fill=tuple((color * 255).astype(int)))

        stream = io.BytesIO()
        im.save(stream, 'png')
        return stream.getvalue()

    def flask(self):
        app = flask.Flask(__name__)

        def gen():
            while True:
                frame = self.png_queue.get()
                yield (b'--frame\r\n'
                       b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n\r\n')

        @app.route('/')
        def get_feed():
            return flask.Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

        app.run(use_reloader=False)

    def show(self, colors):
        self.png_queue.put(self.png(colors))

    # def make_fig_mpl(self, color_list):
    #     coords = np.array([self.triangle_patch([p.center_x, p.center_y], p.orientation + np.pi / 2, 150)
    #                        for p in self.layout])
    #     t = [plt.Polygon(coord, facecolor=tuple(color)) for (coord, color) in zip(coords, color_list)]
    #     xlim = np.min(coords[:, :, 0]), np.max(coords[:, :, 0])
    #     ylim = np.min(coords[:, :, 1]), np.max(coords[:, :, 1])
    #     fig = plt.figure(figsize=(15, 15))
    #     ax = fig.add_subplot(111, aspect='equal')
    #     ax.set_xlim(*xlim)
    #     ax.set_ylim(*ylim)
    #     for tr in t:
    #         ax.add_patch(tr)
    #     return fig
    #
    # def png_mpl(self, color_list):
    #     fig = self.make_fig_mpl(color_list)
    #
    #     buf = io.BytesIO()
    #     fig.savefig(buf, format='png')
    #     buf.seek(0)
    #     return buf.getvalue()
