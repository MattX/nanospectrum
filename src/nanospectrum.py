import argparse

from engine import Engine
from recorder import MikeRecorder, FileRecorder
from visualizations.power import PowerVisualization
from visualizations.bar import BarVisualization
from backends.nanoleaf import NanoleafBackend
from backends.web import WebBackend
from managers import nanoleaf, dummy

RATE = 44100

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help='Nanoleaf IP address')
    parser.add_argument('-p', '--port', help='Nanoleaf port', type=int, default=16021)
    parser.add_argument('-t', '--token-file', help='File with token', default="key")
    parser.add_argument('-m', '--color-map', help='Matplotlib color map', default="jet")
    parser.add_argument('-s', '--simulate',
                        help='Do not connect with actual Nanoleaf. You must specify the number of panels to emulate.',
                        type=int)
    parser.add_argument('-f', '--file', help='A file to read instead of listening for microphone input')
    args = parser.parse_args()

    if args.simulate is not None:
        manager = dummy.DummyManager(args.simulate)
    else:
        manager = nanoleaf.NanoleafManager(args.ip, args.port, open(args.token_file).read().strip())
    nanoleaf_backend = NanoleafBackend(manager)
    web_backend = WebBackend(manager)

    visualization = BarVisualization(manager)

    if args.file is not None:
        recorder = FileRecorder(args.file)
    else:
        recorder = MikeRecorder()

    engine = Engine(recorder, manager, RATE, 0.05, visualization, [
        nanoleaf_backend,
        # web_backend,
    ])
    engine.start()
