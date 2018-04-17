import argparse

from engine import Engine
from backends.nanoleaf_backend import NanoleafBackend
from nanoleaf_manager import NanoleafManager


RATE = 16000

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', help='Nanoleaf IP address')
    parser.add_argument('-p', '--port', help='Nanoleaf port', type=int, default=16021)
    parser.add_argument('-f', '--token-file', help='File with token', default="key")
    parser.add_argument('-m', '--color-map', help='Matplotlib color map', default="inferno")
    args = parser.parse_args()

    manager = NanoleafManager(args.ip, args.port, open(args.token_file).read().strip(), args.color_map)
    nanoleaf_backend = NanoleafBackend(manager)

    engine = Engine(args.color_map, manager, RATE, [nanoleaf_backend])
    engine.start()
