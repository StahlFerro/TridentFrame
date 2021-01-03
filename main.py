from __future__ import print_function
import sys
import random
import string
from typing import List
import os
import signal
import time
import click
import json

from pycore.inspect_ops import inspect_sequence, inspect_general, _inspect_smart
from pycore.create_ops import create_aimg
from pycore.split_ops import split_aimg
from pycore.sprite_ops import _build_spritesheet, _slice_spritesheet
from pycore.modify_ops import modify_aimg
from pycore.core_funcs.criterion import CriteriaBundle, CreationCriteria, SplitCriteria, ModificationCriteria, SpritesheetBuildCriteria, SpritesheetSliceCriteria, GIFOptimizationCriteria, APNGOptimizationCriteria
from pycore.core_funcs.utility import _purge_directory, util_generator, util_generator_shallow
from pycore.core_funcs.config import ABS_CACHE_PATH, ABS_TEMP_PATH, get_bufferfile_content


IS_FROZEN = getattr(sys, 'frozen', False)

@click.group()
def cli():
    pass


# class API(object):
@cli.command("echo")
@click.argument('msg')
def echo(msg):
    print(msg)
    return f"{msg} echoed"


@cli.command("inspect-one")
@click.argument('image_path')
@click.option('--filter', required=False, type=click.Choice(['static', 'animated'], case_sensitive=False))
def inspect_one(image_path, filter=""):
    """Inspect a single image and then return its information"""

    info = inspect_general(image_path, filter)
    if (info):
        info = json.dumps({"data": info})
        print(info)


@cli.command("inspect-many")
def inspect_many():
    """ Inspect a sequence of images and then return their information.
        Intermediary buffer file is used to avoid char limit of command lines
    """
    image_paths = get_bufferfile_content()
    info = inspect_sequence(image_paths)
    if (info):
        info = json.dumps({"data": info})
        print(info)


@cli.command("inspect-smart")
@click.argument('image_path')
def inspect_smart(image_path):
    """Inspect a sequence of images and then return their information"""
    info = _inspect_smart(image_path)
    if (info):
        info = json.dumps({"data": info})
        print(info)


def combine_image(self, image_paths, out_dir, filename, vals: dict):
    """Combine a sequence of images into a GIF/APNG"""
    # raise Exception(image_paths, out_dir, filename, fps, extension, fps, reverse, transparent)
    if not image_paths and not out_dir:
        raise Exception("Please load the images and choose the output folder!")
    elif not image_paths:
        raise Exception("Please load the images!")
    elif not out_dir:
        raise Exception("Please choose the output folder!")
    crbundle = CriteriaBundle({
        "create_aimg": CreationCriteria(vals),
        "gif_opt": GIFOptimizationCriteria(vals),
        "apng_opt": APNGOptimizationCriteria(vals)
    })
    return create_aimg(image_paths, out_dir, filename, crbundle)


def split_image(self, image_path, out_dir, vals):
    """Split all the frames of a GIF/APNG into a sequence of images"""
    if not image_path and not out_dir:
        raise Exception("Please load a GIF or APNG and choose the output folder!")
    elif not image_path:
        raise Exception("Please load a GIF or APNG!")
    elif not out_dir:
        raise Exception("Please choose an output folder!")
    criteria = SplitCriteria(vals)
    return split_aimg(image_path, out_dir, criteria)


def modify_image(self, image_path, out_dir, vals):
    """Modify the criteria and behavior of a GIF/APNG"""
    if not image_path and not out_dir:
        raise Exception("Please load a GIF or APNG and choose the output folder!")
    elif not image_path:
        raise Exception("Please load a GIF or APNG!")
    elif not out_dir:
        raise Exception("Please choose an output folder!")
    criteria = ModificationCriteria(vals)
    crbundle = CriteriaBundle({
        'modify_aimg': ModificationCriteria(vals),
        'gif_opt': GIFOptimizationCriteria(vals),
        'apng_opt': APNGOptimizationCriteria(vals),
    })
    return modify_aimg(image_path, out_dir, crbundle)
    

def build_spritesheet(self, image_paths, out_dir, filename, vals: dict):
    """Build a spritesheet using the specified sequence of images"""
# def build_spritesheet(self, image_paths, input_mode, out_dir, filename, width, height, tiles_per_row, off_x, off_y, pad_x, pad_y, preserve_alpha):
    if not image_paths and not out_dir:
        raise Exception("Please load the images and choose the output folder!")
    elif not image_paths:
        raise Exception("Please load the images!")
    elif not out_dir:
        raise Exception("Please choose the output folder!")
    criteria = SpritesheetBuildCriteria(vals)
    # raise Exception(criteria.__dict__)
    # yield {"msg": "yo"}
    return _build_spritesheet(image_paths, out_dir, filename, criteria)


def slice_spritesheet(self, image_path, out_dir, filename, vals: dict):
    """Slice a spritesheet into individual sections"""
    if not image_path and not out_dir:
        raise Exception("Please load the spritesheet and choose the output folder!")
    elif not image_path:
        raise Exception("Please load the spritesheet!")
    elif not out_dir:
        raise Exception("Please choos the output folder")
    criteria = SpritesheetSliceCriteria(vals)
    return _slice_spritesheet(image_path, out_dir, filename, criteria)


def purge_cache_temp(self):
    """Remove cache and temp directories"""
    _purge_directory(ABS_TEMP_PATH())
    _purge_directory(ABS_CACHE_PATH())
    return "Cache and temp evaporated"


def print_cwd(self):
    """Dev method for displaying python cwd"""
    msg = {
        "os.getcwd()": os.getcwd(),
        "sys.executable": sys.executable,
        "__file__": __file__,
        "IS_FROZEN": IS_FROZEN
    }
    return msg


def test_generator(self):
    return util_generator()


# class GracefullKiller:
#     def __init__(self, SERVER: zerorpc.Server):
#         self.SERVER = SERVER
#         signal.signal(signal.SIGINT, self.exit_gracefully)
#         signal.signal(signal.SIGTERM, self.exit_gracefully)
#         # print(self.SERVER)
    
#     def exit_gracefully(self, signum, frame):
#         print(f"{signum} Closing server...")
#         self.SERVER.close()


def main():
    pass
    # port = '42069'
    # # print(port)
    # handle_execpath()
    # # port = argv
    # address = f"tcp://127.0.0.1:{port}"
    # SERVER: zerorpc.Server = zerorpc.Server(API())
    # SERVER.debug = True
    # SERVER.bind(address)
    # print(f"Starting TridentFrame's imaging engine on {address}")
    # # killer = GracefullKiller(SERVER)
    # SERVER.run()


def handle_execpath():
    if IS_FROZEN:
        frozen_dir = os.path.dirname(sys.executable)
        os.chdir(frozen_dir)


if __name__ == "__main__":
    # port = sys.argv[-1]
    cli()
    # main(port)
