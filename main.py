from __future__ import print_function
import sys
import random
import string

import zerorpc

from pybrain.inspect_ops import _inspect_image, _inspect_sequence
from pybrain.render_ops import _split_image, _combine_image


class API(object):

    def inspect_image(self, image_path):
        info = _inspect_image(image_path)
        return info

    def inspect_sequence(self, dir_path):
        info = _inspect_sequence(dir_path)
        return info

    def combine_image(self, dir_path, out_path):
        res = _combine_image(dir_path, out_path)
        return res

    def split_image(self, image_path, out_path):
        res = _split_image(image_path, out_path)
        return res


def parse_port():
    return 4242


def main():
    address = f"tcp://127.0.0.1:{parse_port()}"
    server = zerorpc.Server(API())
    server.bind(address)
    print(f"Start running on {address}")
    print(server.run())


if __name__ == "__main__":
    main()
