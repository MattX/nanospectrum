import argparse

from engine import Engine
from recorder import MikeRecorder, FileRecorder
from visualizations.power import PowerVisualization
from visualizations.bar import BarVisualization
from backends.nanoleaf import NanoleafBackend
from backends.sdl import SdlBackend
from managers import nanoleaf, dummy

RATE = 44100

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help='Aurora IP address')
    parser.add_argument('-p', '--port', help='Aurora port', type=int, default=16021)
    parser.add_argument('-t', '--token-file', help='File containing Aurora token', default="key")
    parser.add_argument('-m', '--color-map', help='Matplotlib color map', default='viridis')
    parser.add_argument('-i', '--simulate',
                        help='Do not connect with actual Nanoleaf. You must specify the number of panels to emulate. '
                             'Implies --sdl.',
                        type=int)
    parser.add_argument('-f', '--file', help='A file to read instead of listening for microphone input')
    parser.add_argument('-s', '--sdl', help='SDL output', action='store_true')
    args = parser.parse_args()

    backends = []

    if args.simulate is not None:
        manager = dummy.DummyManager(args.simulate)
        args.sdl = True
    else:
        manager = nanoleaf.NanoleafManager(args.ip, args.port, open(args.token_file).read().strip())
        backends += [NanoleafBackend(manager)]

    if args.sdl:
        backends.append(SdlBackend(manager))

    visualization = PowerVisualization(250, 1000, RATE, args.color_map)

    if args.file is not None:
        recorder = FileRecorder(args.file)
    else:
        recorder = MikeRecorder()

    engine = Engine(recorder, manager, RATE, 0.05, visualization, backends)
    engine.start()
