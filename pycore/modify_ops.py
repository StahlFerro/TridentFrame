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

from .core_funcs.config import (
    IMG_EXTS,
    ANIMATED_IMG_EXTS,
    STATIC_IMG_EXTS,
    get_absolute_cache_path,
    get_absolute_temp_path,
    imager_exec_path,
)
from .core_funcs.criterion import (
    CriteriaBundle,
    CreationCriteria,
    SplitCriteria,
    ModificationCriteria,
    APNGOptimizationCriteria,
)
from .core_funcs.utility import (
    _mk_temp_dir,
    _reduce_color,
    _unoptimize_gif,
    _log,
    shout_indices,
)
from .bin_funcs.imager_api import gifsicle_render, imagemagick_render, APNGOptAPI
from .bin_funcs.arg_builder import gifsicle_mod_args, imagemagick_args
from .create_ops import create_aimg
from .split_ops import split_aimg, _fragment_gif_frames, _fragment_apng_frames


def rebuild_aimg(img_path: str, out_dir: str, crbundle: CriteriaBundle):
    mod_criteria = crbundle.modify_aimg
    apngopt_criteria = crbundle.apng_opt_criteria
    frames_dir = _mk_temp_dir(prefix_name="rebuild_aimg")
    # is_unoptimized = mod_criteria.is_unoptimized or mod_criteria.apng_is_unoptimized or mod_criteria.change_format()
    split_criteria = SplitCriteria(
        {
            "pad_count": 6,
            "color_space": "",
            "is_duration_sensitive": True,
            "is_unoptimized": True,
            "new_name": "",
            "will_generate_delay_info": False,
        }
    )
    frame_paths = yield from split_aimg(img_path, frames_dir, split_criteria)
    yield {"MOD split frames": frame_paths}
    # if mod_criteria.is_reversed:
    #     frames.reverse()
    # pq_args = pngquant_args(apngopt_criteria)
    if mod_criteria.format == "PNG" and pq_args:
        yield {"DEBUG": "PNG QUANTIZATION SELECTED"}
        frame_paths = pngquant_render(pq_args, frame_paths)
        yield {"QUANTPATHS": frame_paths}
    ds_fps = mod_criteria.orig_frame_count_ds / mod_criteria.orig_loop_duration
    # ds_delay = 1 / ds_fps
    ds_delay = mod_criteria.delay
    ds_fps = mod_criteria.fps
    yield {"NEW DELAY": ds_delay}
    create_criteria = CreationCriteria(
        {
            "name": mod_criteria.name,
            "fps": ds_fps,
            "delay": ds_delay,
            "format": mod_criteria.format,
            "is_reversed": mod_criteria.is_reversed,
            "preverse_alpha": True,
            "flip_x": mod_criteria.flip_x,  # Flipping horizontally is handled by gifsicle
            "flip_y": mod_criteria.flip_y,  # Flipping vertically is handled by gifsicle
            "width": mod_criteria.width,
            "height": mod_criteria.height,
            "loop_count": mod_criteria.loop_count,
            "start_frame": 1,
            "reverse": mod_criteria.is_reversed,
            "rotation": mod_criteria.rotation,
        }
    )
    yield {"e": create_criteria.name}
    crbundle = CriteriaBundle({"create_aimg_criteria": create_criteria})
    new_image_path = yield from create_aimg(frame_paths, out_dir, create_criteria.name, crbundle)
    yield {"new_image_path": new_image_path}
    return new_image_path


def modify_aimg(img_path: str, out_dir: str, crbundle: CriteriaBundle):
    criteria = crbundle.modify_aimg
    gifopt_criteria = crbundle.gif_opt_criteria
    apngopt_criteria = crbundle.apng_opt_criteria
    img_path = os.path.abspath(img_path)
    # raise Exception(img_path, out_dir, criteria)
    if not os.path.isfile(img_path):
        raise Exception("Cannot Preview/Modify the image. The original file in the system may been removed.")
    out_dir = os.path.abspath(out_dir)
    full_name = f"{criteria.name}.{criteria.format.lower()}"
    orig_full_name = f"{criteria.name}.{criteria.orig_format.lower()}"
    # temp_dir = _mk_temp_dir(prefix_name="temp_mods")
    # temp_save_path = os.path.join(temp_dir, full_name)
    out_full_path = os.path.join(out_dir, full_name)
    orig_out_full_path = os.path.join(out_dir, orig_full_name)
    yield {"OUTFULLPATH": f"{out_full_path}"}
    sicle_args = gifsicle_mod_args(criteria, gifopt_criteria)
    magick_args = imagemagick_args(gifopt_criteria)
    pq_args = pngquant_args(apngopt_criteria)
    # yield sicle_args
    target_path = str(img_path)
    total_ops = 0
    yield {"CHANGE FORMAT???": criteria.change_format()}
    if criteria.change_format():
        if criteria.format == "PNG":
            # if sicle_args:
            #     target_path = yield from _gifsicle_modify(sicle_args, target_path, orig_out_full_path, total_ops)
            # if magick_args:
            #     target_path = yield from _imagemagick_modify(magick_args, target_path, orig_out_full_path, total_ops, len(sicle_args))
            # yield {"preview_path": target_path}
            yield {"msg": f"Changing format ({criteria.orig_format} -> {criteria.format})"}
            target_path = yield from rebuild_aimg(target_path, out_dir, crbundle)
            if aopt_args:
                target_path = yield from APNGOptAPI.optimize_apng(
                    aopt_args,
                    target_path,
                    out_full_path,
                    total_ops,
                    len(sicle_args) + len(magick_args),
                )
        elif criteria.format == "GIF":
            yield {"msg": f"Changing format ({criteria.orig_format} -> {criteria.format})"}
            target_path = yield from rebuild_aimg(target_path, out_dir, crbundle)
            out_full_path = str(target_path)
            if sicle_args:
                target_path = yield from gifsicle_render(sicle_args, target_path, out_full_path, total_ops)
            if magick_args:
                target_path = yield from imagemagick_render(
                    magick_args, target_path, out_full_path, total_ops, len(sicle_args)
                )
            # yield {"preview_path": target_path}
    else:
        if criteria.orig_format == "GIF":
            if criteria.gif_mustsplit_alteration():
                target_path = yield from rebuild_aimg(target_path, out_dir, crbundle)
            if sicle_args or criteria.renamed():
                target_path = yield from gifsicle_render(sicle_args, target_path, orig_out_full_path, total_ops)
            if magick_args:
                target_path = yield from imagemagick_render(
                    magick_args,
                    target_path,
                    orig_out_full_path,
                    total_ops,
                    len(sicle_args),
                )
            # yield {"preview_path": target_path}
        elif criteria.orig_format == "PNG":
            if criteria.apng_mustsplit_alteration() or pq_args or apngopt_criteria.is_unoptimized:
                target_path = yield from rebuild_aimg(target_path, out_dir, crbundle)
            if aopt_args:
                yield {"MSGGGGGGGGGGGGG": "AOPT ARGS"}
                target_path = yield from APNGOptAPI.optimize_apng(
                    aopt_args,
                    target_path,
                    out_full_path,
                    total_ops,
                    len(sicle_args) + len(magick_args),
                )
                # elif criteria.renamed():
                #     yield {"MSGGGGGGGGGGGGG": "RENAME"}
                if target_path != out_full_path:
                    shutil.copy(target_path, out_full_path)
    yield {"preview_path": target_path}

    yield {"CONTROL": "MOD_FINISH"}
