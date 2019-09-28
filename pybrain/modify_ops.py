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

from .config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, ABS_CACHE_PATH, gifsicle_exec, imagemagick_exec
from .criterion import ModificationCriteria
from .utility import _mk_temp_dir, _reduce_color, _unoptimize_gif, _log, _restore_disposed_frames


def modify_aimg(img_path: str, out_dir: str, criteria: ModificationCriteria):
    img_path = os.path.abspath(img_path)
    if not os.path.isfile(img_path):
        raise Exception("Oi skrubman the path here seems to be a bloody directory, should've been a file")
    out_dir = os.path.abspath(out_dir)
    full_name = f"{criteria.name}.{criteria.format.lower()}"
    # temp_dir = _mk_temp_dir(prefix_name="temp_mods")
    # temp_save_path = os.path.join(temp_dir, full_name)
    out_full_path = os.path.join(out_dir, full_name)
    sicle_args = _generate_gifsicle_args(criteria)
    magick_args = _generate_imagemagick_args(criteria)
    # yield sicle_args
    if not (sicle_args and magick_args): 
        yield {"preview_path": img_path}
    elif sicle_args:
        target_path = str(img_path)
        for index, (arg, description) in enumerate(sicle_args, start=1):
            yield {"msg": f"index {index}, arg {arg}, description: {description}"}
            cmdlist = [gifsicle_exec(), arg, f'"{target_path}"', "--output", f'"{out_full_path}"']
            cmd = ' '.join(cmdlist)
            yield {"msg": f"cmd: {cmd}"}
            yield {"msg": f"[{index}/{len(sicle_args)}] {description}"}
            subprocess.run(cmd, shell=True)
            if target_path != out_full_path:
                target_path = out_full_path
        yield {"preview_path": out_full_path}
    yield {"msg": "Finished!"}


def _generate_gifsicle_args(criteria: ModificationCriteria):
    args = []
    if criteria.must_resize():
        args.append((f"--resize={criteria.width}x{criteria.height}", "Resizing image..."))
    if criteria.orig_delay != criteria.delay:
        args.append((f"--delay={criteria.delay * 100}", f"Setting per-frame delay to {criteria.delay}"))
    if criteria.is_optimized and criteria.optimization_level:
        args.append((f"--optimize={criteria.optimization_level}", f"Optimizing image with level, {criteria.optimization_level}..."))
    if criteria.is_lossy and criteria.lossy_value:
        args.append((f"--lossy={criteria.lossy_value}", f"Lossy compressing with value: {criteria.lossy_value}..."))
    if criteria.is_reduced_color and criteria.color_space:
        args.append((f"--colors={criteria.color_space}", f"Reducing colors to: {criteria.color_space}..."))
    if criteria.flip_x:
        args.append(("--flip-horizontal", "Flipping image horizontally..."))
    if criteria.flip_y:
        args.append((f"--flip-vertical", "Flipping image vertically..."))
    return args


def _generate_imagemagick_args(criteria: ModificationCriteria):
    args = []
    if not criteria.rotation:
        args.append(f"-rotation {criteria.rotation}")
    return args