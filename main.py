from __future__ import print_function
import sys
import random
import string
from typing import List

import zerorpc

from pybrain.inspect_ops import _inspect_image, _inspect_sequence
from pybrain.render_ops import split_aimg, create_aimg, _delete_temp_images, create_spritesheet
from pybrain.config import CreationCriteria, SplitCriteria


class API(object):

    def inspect_image(self, image_path):
        info = _inspect_image(image_path)
        return info

    def inspect_sequence(self, dir_path):
        info = _inspect_sequence(dir_path)
        return info

    def combine_image(self, image_paths, out_dir, filename, fps, extension, width, height, reverse, transparent, flip_h, flip_v):
        # raise Exception(image_paths, out_dir, filename, fps, extension, fps, reverse, transparent)
        if not image_paths and not out_dir:
            raise Exception("Please load the sequences and choose the output folder!")
        elif not image_paths:
            raise Exception("Please load the sequences!")
        elif not out_dir:
            raise Exception("Please choose the output folder!")
        criteria = CreationCriteria(fps, extension, reverse, transparent).transform(width, height, flip_h, flip_v)
        res = create_aimg(image_paths, out_dir, filename, criteria)
        return res

    def split_image(self, image_path, out_dir, pad_count):
        if not image_path and not out_dir:
            raise Exception("Please load a GIF or APNG and choose the output folder!")
        elif not image_path:
            raise Exception("Please load a GIF or APNG!")
        elif not out_dir:
            raise Exception("Please choose an output folder!")
        criteria = SplitCriteria(pad_count)
        res = split_aimg(image_path, out_dir, criteria)
        return res

    def delete_temp_images(self):
        res = _delete_temp_images()
        return res

    def create_sprsheet(self, image_paths, out_dir, filename):
        if not image_paths and not out_dir:
            raise Exception("Please load the sequences and choose the output folder!")
        elif not image_paths:
            raise Exception("Please load the sequences!")
        elif not out_dir:
            raise Exception("Please choose the output folder!")
        create_spritesheet(image_paths, out_dir, filename)


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
