import os
import io
import string
import shutil
import math
import time
import subprocess
import tempfile
from random import choices
from pprint import pprint
from urllib.parse import urlparse
from typing import List, Dict, Tuple
from datetime import datetime

from PIL import Image
from apng import APNG, PNG
from hurry.filesize import size, alternative

from .config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, CreationCriteria, SplitCriteria, SpritesheetBuildCriteria, SpritesheetSliceCriteria, ABS_CACHE_PATH, gifsicle_exec
from .utility import _mk_temp_dir, _unoptimize_gif, _get_gif_delay_ratios


def _unoptimize_gif(gif_path) -> str:
    """ Perform GIF unoptimization using Gifsicle, in order to obtain the true singular frames for Splitting purposes. Returns the path of the unoptimized GIF """
    print("Performing unoptimization...")
    executable = gifsicle_exec()
    temp_dir = _mk_temp_dir(prefix_name="unoptimized_gif")
    pure_gif_path = os.path.join(temp_dir, os.path.basename(gif_path))
    args = [executable, "-b", "--unoptimize", gif_path, "--output", pure_gif_path]
    cmd = ' '.join(args)
    print(cmd)
    subprocess.run(cmd, shell=True)
    return pure_gif_path


def _get_gif_delay_ratios(gif_path: str, duration_sensitive: bool = False) -> List[Tuple[str, str]]:
    """ Returns a list of dual-valued tuples, first value being the frame numbers of the GIF, second being the ratiko of the frame's delay to the lowest delay"""
    with Image.open(gif_path) as gif:
        indices = list(range(0, gif.n_frames))
        durations = []
        for i in indices:
            gif.seek(i)
            durations.append(gif.info['duration'])
        min_duration = min(durations)
        if duration_sensitive:
            ratios = [dur//min_duration for dur in durations]
        else:
            ratios = [1 for dur in durations]
        indexed_ratios = list(zip(indices, ratios))
    return indexed_ratios


def _split_gif(gif_path: str, out_dir: str, criteria: SplitCriteria) -> List[str]:
    """ Split GIF. Returns a list of absolute path of each split'd frames """
    unop_gif_path = _unoptimize_gif(gif_path)
    print('unop gif path', unop_gif_path)
    executable = gifsicle_exec()
    orig_name = os.path.splitext(os.path.basename(unop_gif_path))[0]
    indexed_ratios = _get_gif_delay_ratios(unop_gif_path, criteria.is_duration_sensitive)
    sequence = 0
    for index, ratio in indexed_ratios:
        selector = f'"#{index}"'
        for n in range(0, ratio):
            save_path = os.path.join(out_dir, f'{orig_name}_{str.zfill(str(sequence), 3)}.png')
            args = [executable, unop_gif_path, selector, "--output", save_path]
            cmd = ' '.join(args)
            subprocess.run(cmd, shell=True)
            sequence += 1


def split_aimg(image_path: str, out_dir: str, criteria: SplitCriteria) -> bool:
    """ Resolves paths, and decide whether to split a GIF or APNG """
    # print(error)
    abspath = os.path.abspath(image_path)
    print(abspath)
    if not os.path.isfile(image_path):
        raise Exception("Oi skrubman the path here seems to be a bloody directory, should've been a file")
    filename = str(os.path.basename(abspath))

    # Custom output dirname and frame names if specified on the cli
    if '.' not in filename:
        raise Exception('Where the fuk is the extension mate?!')

    fname, ext = os.path.splitext(filename)
    ext = str.lower(ext[1:])
    # raise Exception(fname, ext)
    if ext not in ANIMATED_IMG_EXTS:
        raise Exception('Only supported extensions are gif and apng. Sry lad')

    out_dir = os.path.abspath(out_dir)
    print(out_dir)
    # Image processing
    if ext == 'gif':
        print(image_path, out_dir, criteria)
        _split_gif(image_path, out_dir, criteria)

    elif ext == 'png':
        img: APNG = APNG.open(filename)
        iframes = img.frames
        pad_count = max(len(str(len(iframes))), 3)
        # print('frames', [(png, control.__dict__) for (png, control) in img.frames][0])
        # with click.progressbar(iframes, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as frames:
        for index, (png, control) in enumerate(iframes):
            # yield f'Splitting APNG... ({index + 1}/{len(iframes)})'
            png.save(os.path.join(out_dir, f"{fname}_{str.zfill(str(index), pad_count)}.png"))
    return True



# if __name__ == "__main__":
#     pprint(_inspect_sequence(""))

    # gs_split("./test/blobsekiro.gif", "./test/sequence/")
    # test()
    # _unoptimize_gif("./test/blobkiro.gif")
