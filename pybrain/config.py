import os
import platform
from typing import Tuple


IMG_EXTS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
STATIC_IMG_EXTS = ['png', 'jpg', 'jpeg', 'bmp', 'gif']
ANIMATED_IMG_EXTS = ['gif', 'png']

CACHE_PATH = './cache/'
ABS_CACHE_PATH = os.path.abspath(CACHE_PATH)


def gifsicle_exec():
    if platform.system() == 'Windows':
        return os.path.abspath("./bin/gifsicle-1.92-win64/gifsicle.exe")
    elif platform.system() == 'Linux':
        return os.path.abspath("./bin/gifsicle-1.92-2+b1_amd64/gifsicle")
    else:
        return False

def imagemagick_exec():
    if platform.system() == 'Windows':
        return os.path.abspath("./bin/ImageMagick-7.0.8-61-win/convert.exe")
    elif platform.system() == 'Linux':
        return os.path.abspath("./bin/ImageMagick-7.0.8-61-unix/convert")


class CreationCriteria():
    """ Contains all of the criterias for Creating an animated image """
    def __init__(self, fps, delay, extension, reverse, transparent):
        try:
            fps = float(fps)
        except Exception as e:
            raise Exception(e)
        self.fps: float = fps
        self.duration: float = round(1000 / fps)
        self.extension: str = extension
        self.reverse: bool = reverse
        self.transparent: bool = transparent
        self.flip_h: bool = False
        self.flip_v: bool = False
    
    def transform(self, resize_width, resize_height, flip_h, flip_v):
        try:
            resize_width = float(resize_width)
            resize_height = float(resize_height)
        except Exception as e:
            raise Exception(e)        
        self.resize_width: int = resize_width
        self.resize_height: int = resize_height
        self.flip_h = flip_h
        self.flip_v = flip_v
        return self


class SplitCriteria():
    """ Contains all of the criterias for Splitting an animated image """

    def __init__(self, pad_count, color_space, is_duration_sensitive=False):
        try:
            pad_count = int(pad_count)
            color_space = int(color_space)
        except Exception as e:
            raise Exception(e)
        self.pad_count: int = pad_count
        self.color_space: int = color_space
        self.is_duration_sensitive: bool = is_duration_sensitive


class ModificationCriteria():
    """ Contains all of the criterias for Modifying the specifications of an animated image """

    def __init__(self, width, height, duration, fps, reduce_color, color_space, new_format, reverse):
        self.width = width
        self.height = height
        self.duration = duration
        self.fps = fps
        self.reduce_color = reduce_color
        self.color_space = color_space
        self.format = new_format
        self.reverse = reverse


class SpritesheetBuildCriteria():
    """ Contains all of the criterias to build a spritesheet """

    def __init__(self, resize_width, resize_height, tiles_per_row, offset_x, offset_y, padding_x, padding_y, preserve_alpha):
        self.resize_width: int = int(resize_height)
        self.resize_height: int = int(resize_height)
        self.tiles_per_row: int = int(tiles_per_row)
        self.offset_x: int = int(offset_x)
        self.offset_y: int = int(offset_y)
        self.padding_x: int = int(padding_x)
        self.padding_y: int = int(padding_y)
        self.preserve_alpha: bool = preserve_alpha


class SpritesheetSliceCriteria():
    """ Contains all of the criterias to slice a spritesheet """

    def __init__(self, tile_x, tile_y, offset_x, offset_y, padding_x, padding_y):
        self.tile_x: int = int(tile_x)
        self.tile_y: int = int(tile_y)
        self.offset_x: int = int(offset_x)
        self.offset_y: int = int(offset_y)
        self.padding_x: int = int(padding_x)
        self.padding_y: int = int(padding_y)
