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

from .config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, ABS_CACHE_PATH, imager_exec_path
from .criterion import CreationCriteria, SplitCriteria, ModificationCriteria
from .utility import _mk_temp_dir, _reduce_color, _unoptimize_gif, _log, _restore_disposed_frames
from .create_ops import create_aimg
from .split_ops import split_aimg


def _gifsicle_modify(sicle_args: List[Tuple[str, str]], target_path: str, out_full_path: str, total_ops: int) -> str:
    gifsicle_path = imager_exec_path('gifsicle')
    for index, (arg, description) in enumerate(sicle_args, start=1):
        yield {"msg": f"index {index}, arg {arg}, description: {description}"}
        cmdlist = [gifsicle_path, arg, f'"{target_path}"', "--output", f'"{out_full_path}"']
        cmd = ' '.join(cmdlist)
        yield {"msg": f"[{index}/{total_ops}] {description}"}
        yield {"cmd": cmd}
        subprocess.run(cmd, shell=True)
        if target_path != out_full_path:
            target_path = out_full_path
    return target_path


def _imagemagick_modify(magick_args: List[Tuple[str, str]], target_path: str, out_full_path: str, total_ops: int, shift_index: int) -> str:
    imagemagick_path = imager_exec_path('imagemagick')
    for index, (arg, description) in enumerate(magick_args, start=1):
        yield {"msg": f"index {index}, arg {arg}, description: {description}"}
        cmdlist = [imagemagick_path, arg, f'"{target_path}"', "--output", f'"{out_full_path}"']
        cmd = ' '.join(cmdlist)
        yield {"msg": f"[{shift_index + index}/{total_ops}] {description}"}
        yield {"cmd": cmd}
        subprocess.run(cmd, shell=True)
        if target_path != out_full_path:
            target_path = out_full_path
    return target_path


def _change_aimg_format(img_path: str, out_dir: str, mod_criteria: ModificationCriteria):
    frames_dir = _mk_temp_dir(prefix_name="formod_frames")
    split_criteria = SplitCriteria({
        'pad_count': 6,
        'color_space': "",
        'is_duration_sensitive': True,
        'is_unoptimized': mod_criteria.is_unoptimized,
    })
    # yield {"msg": split_criteria.__dict__}
    yield from split_aimg(img_path, frames_dir, split_criteria)
    frames = [str(os.path.join(frames_dir, f)) for f in os.listdir(frames_dir)]
    yield {"msg": frames}
    ds_fps = mod_criteria.orig_frame_count_ds / mod_criteria.orig_loop_duration
    ds_delay = 1 / ds_fps
    create_criteria = CreationCriteria({
        'fps': ds_fps,
        'delay': ds_delay,
        'format': mod_criteria.format,
        'is_reversed': mod_criteria.is_reversed,
        'is_transparent': True,
        'flip_x': mod_criteria.flip_x,
        'flip_y': mod_criteria.flip_y,
        'width': mod_criteria.width,
        'height': mod_criteria.height,
    })
    new_image = yield from create_aimg(frames, out_dir, os.path.basename(img_path), create_criteria)
    return new_image


def modify_aimg(img_path: str, out_dir: str, criteria: ModificationCriteria):
    img_path = os.path.abspath(img_path)
    if not os.path.isfile(img_path):
        raise Exception("Cannot Preview/Modify the image. The original file in the system may been removed.")
    out_dir = os.path.abspath(out_dir)
    full_name = f"{criteria.name}.{criteria.orig_format.lower()}"
    # temp_dir = _mk_temp_dir(prefix_name="temp_mods")
    # temp_save_path = os.path.join(temp_dir, full_name)
    out_full_path = os.path.join(out_dir, full_name)
    # yield {"msg": f"OUT FULL PATH: {out_full_path}"}
    sicle_args = _generate_gifsicle_args(criteria)
    magick_args = _generate_imagemagick_args(criteria)
    apngopt_args = _generate_apngopt_args(criteria)
    # yield sicle_args
    target_path = str(img_path)
    total_ops = len(sicle_args) + len(magick_args)

    if criteria.change_format():
        if criteria.orig_format == "GIF":
            if sicle_args:
                target_path = yield from _gifsicle_modify(sicle_args, target_path, out_full_path, total_ops)
            if magick_args:
                target_path = yield from _imagemagick_modify(magick_args, target_path, out_full_path, total_ops, len(sicle_args))
            yield {"preview_path": target_path}
            yield {"msg": f"Changing format ({criteria.orig_format} -> {criteria.format})"}
            target_path = yield from _change_aimg_format(target_path, out_dir, criteria)
        elif criteria.orig_format == "PNG":
            yield {"msg": f"Changing format ({criteria.orig_format} -> {criteria.format})"}
            target_path = yield from _change_aimg_format(target_path, out_dir, criteria)
            out_full_path = str(target_path)
            if sicle_args:
                target_path = yield from _gifsicle_modify(sicle_args, target_path, out_full_path, total_ops)
            if magick_args:
                target_path = yield from _imagemagick_modify(magick_args, target_path, out_full_path, total_ops, len(sicle_args))             
            yield {"preview_path": target_path}
    else:
        if criteria.orig_format == "GIF":
            if sicle_args:
                target_path = yield from _gifsicle_modify(sicle_args, target_path, out_full_path, total_ops)
            if magick_args:
                target_path = yield from _imagemagick_modify(magick_args, target_path, out_full_path, total_ops, len(sicle_args))
            yield {"preview_path": target_path}
        elif criteria.orig_format == "PNG":
            yield {"preview_path": target_path}

    yield {"CONTROL": "MOD_FINISH"}

            
    # if sicle_args:
    #     target_path = yield from _gifsicle_modify(sicle_args, target_path, out_full_path, total_ops)
    #     # for index, (arg, description) in enumerate(sicle_args, start=1):
    #     #     yield {"msg": f"index {index}, arg {arg}, description: {description}"}
    #     #     cmdlist = [gifsicle_exec(), arg, f'"{target_path}"', "--output", f'"{out_full_path}"']
    #     #     cmd = ' '.join(cmdlist)
    #     #     yield {"msg": f"cmd: {cmd}"}
    #     #     yield {"msg": f"[{index}/{total_ops}] {description}"}
    #     #     subprocess.run(cmd, shell=True)
    #     #     if target_path != out_full_path:
    #     #         target_path = out_full_path
    # if magick_args:
    #     target_path = yield from _imagemagick_modify(magick_args, target_path, out_full_path, total_ops, len(sicle_args))
    #     # for index, (arg, description) in enumerate(magick_args, start=1):
    #     #     yield {"msg": f"index {index}, arg {arg}, description: {description}"}
    #     #     cmdlist = [imagemagick_exec(), arg, f'"{target_path}"', "--output", f'"{out_full_path}"']
    #     #     cmd = ' '.join(cmdlist)
    #     #     yield {"msg": f"cmd: {cmd}"}
    #     #     yield {"msg": f"[{len(sicle_args) + index}/{total_ops}] {description}"}
    #     #     subprocess.run(cmd, shell=True)
    #     #     if target_path != out_full_path:
    #     #         target_path = out_full_path

    # yield {"preview_path": target_path}
    # if criteria.change_format():
    #     yield {"msg": f"Changing format ({criteria.orig_format} -> {criteria.format})"}
    #     yield from _change_aimg_format(target_path, "./temp", criteria)


def _generate_gifsicle_args(criteria: ModificationCriteria) -> List[Tuple[str, str]]:
    args = []
    if criteria.must_resize():
        args.append((f"--resize={criteria.width}x{criteria.height}", "Resizing image..."))
    if criteria.orig_delay != criteria.delay:
        args.append((f"--delay={criteria.delay * 100}", f"Setting per-frame delay to {criteria.delay}"))
    if criteria.is_optimized and criteria.optimization_level:
        args.append((f"--optimize={criteria.optimization_level}", f"Optimizing image with level {criteria.optimization_level}..."))
    if criteria.is_lossy and criteria.lossy_value:
        args.append((f"--lossy={criteria.lossy_value}", f"Lossy compressing with value: {criteria.lossy_value}..."))
    if criteria.is_reduced_color and criteria.color_space:
        args.append((f"--colors={criteria.color_space}", f"Reducing colors to: {criteria.color_space}..."))
    if criteria.flip_x:
        args.append(("--flip-horizontal", "Flipping image horizontally..."))
    if criteria.flip_y:
        args.append((f"--flip-vertical", "Flipping image vertically..."))
    if criteria.orig_loop_count != criteria.loop_count:
        loop_count = criteria.loop_count
        loop_arg = "--loopcount"
        if (not loop_count or loop_count == 0):
            loop_arg = "--loopcount"
        elif (loop_count == 1):
            loop_arg = '--no-loopcount'
        elif (loop_count > 1):
            loop_arg = f'--loopcount={loop_count - 1}'
        args.append((loop_arg, f"Changing loop count to {loop_count or 'Infinite'}..."))
    return args


def _generate_imagemagick_args(criteria: ModificationCriteria) -> List[Tuple[str, str]]:
    args = []
    if criteria.is_unoptimized:
        args.append(("-coalesce", "Unoptimizing GIF..."))
    if criteria.rotation:
        args.append((f"-rotate {criteria.rotation}", f"Rotating image {criteria.rotation} degrees..."))
    return args


def _generate_apng_dis(criteria: ModificationCriteria) -> List[Tuple[str, str]]:
    args = []
    

def _generate_apngopt_args(criteria: ModificationCriteria) -> List[Tuple[str, str]]:
    args = []
    if criteria.apng_is_optimized:
        args.append((f'-z{criteria.apng_optimization_level}', f'Optimizing image with level {criteria.apng_optimization_level}...'))
    return args


def _generate_pngquant_args(criteria: ModificationCriteria) -> List[Tuple[str, str]]:
    args = []
    # if criteria.apng_is_lossy:
        # args.append(())
    return args