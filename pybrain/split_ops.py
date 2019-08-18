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

from .config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, SplitCriteria, ABS_CACHE_PATH, gifsicle_exec, imagemagick_exec
from .utility import _mk_temp_dir, _reduce_color, _unoptimize_gif, _log, _restore_disposed_frames


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


def _split_gif_imagemagick(unop_gif_path: str, out_dir: str, criteria: SplitCriteria):
    orig_name = os.path.splitext(os.path.basename(unop_gif_path))[0]
    indexed_ratios = _get_gif_delay_ratios(unop_gif_path, criteria.is_duration_sensitive)
    total_ratio = sum([ir[1] for ir in indexed_ratios])
    sequence = 0
    gifragment_paths = []
    for index, ratio in indexed_ratios[0:80]:
        selector = f"'{unop_gif_path}[{index}]'"
        for n in range(0, ratio):
            yield f"Splitting GIF... ({sequence + 1}/{total_ratio})"
            save_path = os.path.join(out_dir, f'{orig_name}_{str.zfill(str(sequence), 3)}.png')
            executable = imagemagick_exec()
            args = [executable, selector, save_path]
            cmd = ' '.join(args)
            # raise Exception(cmd)
            yield cmd
            subprocess.run(args)
            # subprocess.run(cmd, shell=True)
            gifragment_paths.append(save_path)
            sequence += 1
            # time.sleep(0.3)


def _split_gif_gifsicle(unop_gif_path: str, out_dir: str, criteria: SplitCriteria):
    orig_name = os.path.splitext(os.path.basename(unop_gif_path))[0]
    indexed_ratios = _get_gif_delay_ratios(unop_gif_path, criteria.is_duration_sensitive)
    total_ratio = sum([ir[1] for ir in indexed_ratios])
    sequence = 0
    gifragment_paths = []
    for index, ratio in indexed_ratios:
        selector = f'"#{index}"'
        for n in range(0, ratio):
            # yield f"Splitting GIF... ({sequence + 1}/{total_ratio})"
            save_path = os.path.join(out_dir, f'{orig_name}_{str.zfill(str(sequence), 3)}.gif')
            args = [gifsicle_exec(), unop_gif_path, selector, "--output", save_path]
            cmd = ' '.join(args)
            subprocess.run(cmd, shell=True)
            gifragment_paths.append(save_path)
            sequence += 1


def _split_gif(gif_path: str, out_dir: str, criteria: SplitCriteria):
    """ Splits GIF. Returns a list of absolute path of each split'd frames. """
    unop_dir = _mk_temp_dir(prefix_name="unop_gif")
    color_space = criteria.color_space
    unop_gif_path = ''
    if color_space == 0:
        yield f"Unoptimizing frames for splitting (GIFs above 10MB will take minutes to process)..."
        unop_gif_path = _unoptimize_gif(gif_path, unop_dir, "imagemagick")
    else:
        yield f"Setting global color palette to {color_space}..."
        if color_space < 2 or color_space > 256:
            raise Exception("Color space must be between 2 and 256!")
        redux_gif_path = _reduce_color(gif_path, unop_dir, color=color_space)
        yield f"Coalescing frames for splitting..."
        unop_gif_path = _unoptimize_gif(redux_gif_path, unop_dir, "gifsicle")
    yield from _split_gif_gifsicle(unop_gif_path, out_dir, criteria)
    yield "Finished!"


def _split_apng(apng_path: str, out_dir: str, name: str, criteria: SplitCriteria):
    img: APNG = APNG.open(apng_path)
    iframes = img.frames
    pad_count = max(len(str(len(iframes))), 3)
    # print('frames', [(png, control.__dict__) for (png, control) in img.frames][0])
    # with click.progressbar(iframes, empty_char=" ", fill_char="█", show_percent=True, show_pos=True) as frames:
    for index, (png, control) in enumerate(iframes):
        yield f'Splitting APNG... ({index + 1}/{len(iframes)})'
        png.save(os.path.join(out_dir, f"{name}_{str.zfill(str(index), pad_count)}.png"))


def split_aimg(image_path: str, out_dir: str, criteria: SplitCriteria) -> bool:
    """ Umbrella function for splitting animated images into individual frames """
    # print(error)
    abspath = os.path.abspath(image_path)
    if not os.path.isfile(abspath):
        raise Exception("Oi skrubman the path here seems to be a bloody directory, should've been a file")
    filename = str(os.path.basename(abspath))

    # Custom output dirname and frame names if specified on the cli
    if '.' not in filename:
        raise Exception('Where the fuk is the extension mate?!')

    name, ext = os.path.splitext(filename)
    ext = str.lower(ext[1:])
    # raise Exception(fname, ext)
    if ext not in ANIMATED_IMG_EXTS:
        raise Exception('Only supported extensions are gif and apng. Sry lad')

    out_dir = os.path.abspath(out_dir)
    print(out_dir)
    # Image processing
    if ext == 'gif':
        print(abspath, out_dir, criteria)
        return _split_gif(abspath, out_dir, criteria)

    elif ext == 'png':
        return _split_apng(abspath, out_dir, name, criteria)


# if __name__ == "__main__":
#     pprint(_inspect_sequence(""))

    # gs_split("./test/blobsekiro.gif", "./test/sequence/")
    # test()
    # _unoptimize_gif("./test/blobkiro.gif")
