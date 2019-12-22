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

from .core_funcs.config import IMG_EXTS, ANIMATED_IMG_EXTS, STATIC_IMG_EXTS, ABS_CACHE_PATH, ABS_TEMP_PATH, imager_exec_path
from .core_funcs.criterion import CreationCriteria, SplitCriteria, ModificationCriteria
from .core_funcs.utility import _mk_temp_dir, _reduce_color, _unoptimize_gif, _log, shout_indices
from .core_funcs.arg_builder import gifsicle_args, imagemagick_args, apngopt_args, pngquant_args
from .create_ops import create_aimg
from .split_ops import split_aimg, _fragment_gif_frames, _fragment_apng_frames


def _gifsicle_modify(sicle_args: List[Tuple[str, str]], target_path: str, out_full_path: str, total_ops: int) -> str:
    yield {"sicle_args": sicle_args}
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
    yield {"magick_args": magick_args}
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


def _apngopt_modify(aopt_args: List[Tuple[str, str]], target_path: str, out_full_path: str, total_ops: int, shift_index: int):
    yield {"aopt_args": aopt_args}
    # apngopt_path = imager_exec_path('apngopt')
    # # cwd = subprocess.check_output('pwd', shell=True).decode('utf-8')
    # cwd = str(os.getcwd())
    # common_path = os.path.commonpath([target_path, out_full_path, apngopt_path])
    # target_rel_path = os.path.relpath(target_path, cwd)
    # out_rel_path = os.path.relpath(out_full_path, cwd)
    # # raise Exception(apngopt_path, common_path, target_rel_path, out_rel_path)
    # # result = subprocess.check_output('pwd', shell=True).decode('utf-8')
    # yield {"cwd": cwd}
    # # yield {"pcwd": os.getcwd()}
    # for index, (arg, description) in enumerate(aopt_args, start=1):
    #     yield {"msg": f"index {index}, arg {arg}, description: {description}"}
    #     cmdlist = [apngopt_path, arg, f'"{target_rel_path}"', f'"{out_rel_path}"']
    #     cmd = ' '.join(cmdlist)
    #     yield {"msg": f"[{shift_index + index}/{total_ops}] {description}"}
    #     yield {"cmd": cmd}
    #     result = subprocess.check_output(cmd, shell=True)
    #     # yield {"out": result}
    #     if target_path != out_full_path:
    #         target_path = out_full_path
    # return target_path
    aopt_dir = _mk_temp_dir(prefix_name='apngopt_dir')
    opt_exec_path = imager_exec_path('apngopt')
    filename = os.path.basename(target_path)
    target_path = shutil.copyfile(target_path, os.path.join(aopt_dir, filename))
    cwd = os.getcwd()
    # common_path = os.path.commonpath([opt_exec_path, target_path])
    target_rel_path = os.path.relpath(target_path, cwd)
    for index, (arg, description) in enumerate(aopt_args, start=1):
        yield {"msg": f"index {index}, arg {arg}, description: {description}"}
        cmdlist = [opt_exec_path, arg, f'"{target_rel_path}"', f'"{target_rel_path}"']
        # raise Exception(cmdlist, out_full_path)
        cmd = ' '.join(cmdlist)
        yield {"msg": f"[{shift_index + index}/{total_ops}] {description}"}
        yield {"cmd": cmd}
        result = subprocess.check_output(cmd, shell=True)
        yield {"out": result}
        # if target_path != out_full_path:
            # target_path = out_full_path
    x = shutil.move(target_path, out_full_path)
    yield {"X": x}
    shutil.rmtree(aopt_dir)
    return out_full_path

    # yield {"aopt_args": aopt_args}
    # opt_dir = _mk_temp_dir(prefix_name='apngopt_dir')
    # apng_name = os.path.basename(target_path)
    # apngopt_path = shutil.copyfile(imager_exec_path('apngopt'), os.path.join(opt_dir, 'apngopt'))
    # apng_copied = os.path.basename(shutil.copyfile(target_path, os.path.join(opt_dir, apng_name)))
    # for index, (arg, description) in enumerate(aopt_args, start=1):
    #     yield {"msg": f"index {index}, arg {arg}, description: {description}"}
    #     cmdlist = [apngopt_path, arg, f'"{apng_copied}"', f'"{apng_copied}"']
    #     # raise Exception(cmdlist, out_full_path)
    #     cmd = ' '.join(cmdlist)
    #     yield {"msg": f"[{shift_index + index}/{total_ops}] {description}"}
    #     yield {"cmd": cmd}
    #     result = subprocess.check_output(cmd, shell=True)
    #     yield {"out": result}
    #     if target_path != out_full_path:
    #         target_path = out_full_path
    # return target_path


# def _internal_gif_reverse(target_path: str, out_full_path: str, mod_criteria: ModificationCriteria, total_ops: int, shift_index: int = 0):
#     frames_dir = _mk_temp_dir(prefix_name="formod_frames")
#     split_criteria = SplitCriteria({
#         'pad_count': 6,
#         'color_space': "",
#         'is_duration_sensitive': True,
#         'is_unoptimized': mod_criteria.is_unoptimized,
#     })
#     # yield {"msg": split_criteria.__dict__}
#     yield from split_aimg(target_path, frames_dir, split_criteria)

# def rebuild_aimg(target_path: str, out_full_path: str, mod_criteria: ModificationCriteria):
#     """ Splits an AIMG into frames, perform modificiation and assemble them back into an AIMG """
#     frames = []
#     split_criteria = SplitCriteria({
#         'pad_count': 6,
#         'color_space': "",
#         'is_duration_sensitive': True,
#         'is_unoptimized': True,
#     })
#     if mod_criteria.orig_format == "GIF":
#         name = os.path.basename(target_path)
#         frames = yield from _fragment_gif_frames(target_path, name, split_criteria)
#     elif mod_criteria.orig_format == "PNG":
#         apng: APNG = APNG.open(target_path)
#         frames = yield from _fragment_apng_frames(apng, split_criteria)
#     if mod_criteria.change_format():
#         if mod_criteria.apng_is_lossy and mod_criteria.apng_lossy_value:
#             frames = _batch_quantize(frames, mod_criteria)

#     shout_nums = shout_indices(len(frames), 5)
#     for index, im in enumerate(frames):
#         if shout_nums.get(index):
#             yield {"msg": f'Modifying APNG... ({shout_nums.get(index)})'}
#         # im.show()
#         # with io.BytesIO() as bytebox:
#         #     png.save(bytebox)
#         #     with Image.open(bytebox) as im:
#         if mod_criteria.flip_x:
#             im = im.transpose(Image.FLIP_LEFT_RIGHT)
#         if mod_criteria.flip_y:
#             im = im.transpose(Image.FLIP_TOP_BOTTOM)
#         if mod_criteria.is_reversed or mod_criteria.must_resize():
#             im = im.resize((mod_criteria.width, mod_criteria.height))
#         newbox = io.BytesIO()
#         im.save(newbox, format="PNG")
#         new_apng.append(PNG.from_bytes(newbox.getvalue()), delay=int(mod_criteria.delay * 1000))
#     new_apng.save(out_full_path)
#     return out_full_path


# def _internal_apng_modify(target_path: str, out_full_path: str, mod_criteria: ModificationCriteria, total_ops: int, shift_index: int = 0):
#     """ Splits the APNG apart into frames, apply modification to each frames, and then compile them back """
#     apng = APNG.open(target_path)
#     new_apng = APNG()
#     yield {"log": "Internal APNG Modification"}
#     split_criteria = SplitCriteria({
#         'pad_count': 6,
#         'color_space': "",
#         'is_duration_sensitive': True,
#         'is_unoptimized': True,
#     })
#     frames = yield from _fragment_apng_frames(apng, split_criteria)
#     if mod_criteria.is_reversed:
#         frames.reverse()
#     if mod_criteria.apng_is_lossy and mod_criteria.apng_lossy_value:
#         frames = yield from _batch_quantize(frames, mod_criteria)
#     shout_nums = shout_indices(len(frames), 5)
#     for index, im in enumerate(frames):
#         if shout_nums.get(index):
#             yield {"msg": f'Modifying APNG... ({shout_nums.get(index)})'}
#         # im.show()
#         # with io.BytesIO() as bytebox:
#         #     png.save(bytebox)
#         #     with Image.open(bytebox) as im:
#         if mod_criteria.flip_x:
#             im = im.transpose(Image.FLIP_LEFT_RIGHT)
#         if mod_criteria.flip_y:
#             im = im.transpose(Image.FLIP_TOP_BOTTOM)
#         if mod_criteria.is_reversed or mod_criteria.must_resize():
#             im = im.resize((mod_criteria.width, mod_criteria.height))
#         newbox = io.BytesIO()
#         im.save(newbox, format="PNG")
#         new_apng.append(PNG.from_bytes(newbox.getvalue()), delay=int(mod_criteria.delay * 1000))
#     new_apng.save(out_full_path)
#     return out_full_path

# def _batch_quantize_images(images: List[Image.Image], criteria: ModificationCriteria):
#     """ Wrapper function to quantize images through their paths """
#     quant_dir = _mk_temp_dir(prefix_name="quant_dir")
#     image_paths = []
#     for index, im in enumerate(images):
#         save_path = os.path.join(quant_dir, f"{str(index).zfill(4)}.png")
#         image_paths = im.save()
#     images = yield from _batch_quantize_paths(image_paths, criteria)

def _batch_quantize_paths(image_paths: List[str], criteria: ModificationCriteria):
    """ Perform PNG quantization on a list of PIL.Image.Images using PNGQuant """
    quantized_frames = []
    pngquant_exec = imager_exec_path("pngquant")
    q_ops = pngquant_args(criteria)
    # quant_dir = _mk_temp_dir(prefix_name="quant_dir")
    shout_nums = shout_indices(len(image_paths), 5)
    for index, ipath in enumerate(image_paths):
        if shout_nums.get(index):
            yield {"msg": f'Quantizing PNG... ({shout_nums.get(index)})'}
        # save_path = os.path.join(quant_dir, f"{index}.png")
        # out_path = os.path.join(quant_dir, f"{index}_quantized.png")
        # yield {"FMODE": fr.mode}
        # fr.save(save_path, "PNG")
        args = [pngquant_exec, ' '.join([q[0] for q in q_ops]), ipath, "--force", "--output", ipath]
        cmd = ' '.join(args)
        # yield {"cmd": cmd}
        result = subprocess.check_output(cmd, shell=True)
        # yield {"out": result}
        # quantized_img = Image.open(ipath)
        # yield {"QMODE": quantized_img.mode}
        # quantized_img = quantized_img.convert("RGBA")
        # quantized_frames.append(quantized_img)
        with Image.open(ipath).convert("RGBA") as rgba_im:
            rgba_im.save(ipath)
        quantized_frames.append(ipath)
    # yield {"ssdsdsssdsd": quantized_frames}
    return quantized_frames

def rebuild_aimg(img_path: str, out_dir: str, mod_criteria: ModificationCriteria):
    frames_dir = _mk_temp_dir(prefix_name="rebuild_aimg")
    # is_unoptimized = mod_criteria.is_unoptimized or mod_criteria.apng_is_unoptimized or mod_criteria.change_format()
    split_criteria = SplitCriteria({
        'pad_count': 6,
        'color_space': "",
        'is_duration_sensitive': True,
        'is_unoptimized': True,
    })
    frame_paths = yield from split_aimg(img_path, frames_dir, split_criteria)
    yield {"frames before": frame_paths}
    # if mod_criteria.is_reversed:
    #     frames.reverse()
    yield {"frames after": frame_paths}
    if mod_criteria.format == 'PNG' and mod_criteria.apng_is_lossy and mod_criteria.apng_lossy_value:
        yield {"DEBUG": "PNG QUANTIZATION SELECTED"}
        frame_paths = yield from _batch_quantize_paths(frame_paths, mod_criteria)
        yield {"QUANTPATHS": frame_paths}
    ds_fps = mod_criteria.orig_frame_count_ds / mod_criteria.orig_loop_duration
    ds_delay = 1 / ds_fps
    create_criteria = CreationCriteria({
        'name': mod_criteria.name,
        'fps': ds_fps,
        'delay': ds_delay,
        'format': mod_criteria.format,
        'is_reversed': mod_criteria.is_reversed,
        'is_transparent': True,
        'flip_x': mod_criteria.flip_x, # Flipping horizontally is handled by gifsicle
        'flip_y': mod_criteria.flip_y, # Flipping vertically is handled by gifsicle
        'width': mod_criteria.width,
        'height': mod_criteria.height,
        'loop_count': mod_criteria.loop_count,
        'reverse': mod_criteria.is_reversed,
        'rotation': mod_criteria.rotation,
    })
    new_image_path = yield from create_aimg(frame_paths, out_dir, os.path.basename(img_path), create_criteria)
    yield {"new_image_path": new_image_path}
    return new_image_path


# def change_aimg_format(img_path: str, out_dir: str, mod_criteria: ModificationCriteria):
#     yield {"DEBUG": [img_path, out_dir]}
#     """ Splits a GIF/APNG into frames, and then recompile them back into an AIMG. Used to change their format, or reverse the animation"""
#     frames_dir = _mk_temp_dir(prefix_name="formod_frames")
#     split_criteria = SplitCriteria({
#         'pad_count': 6,
#         'color_space': "",
#         'is_duration_sensitive': True,
#         'is_unoptimized': mod_criteria.is_unoptimized,
#     })
#     # yield {"msg": split_criteria.__dict__}
#     yield from split_aimg(img_path, frames_dir, split_criteria)
#     frames = [str(os.path.join(frames_dir, f)) for f in sorted(os.listdir(frames_dir))]
#     yield {"frames_dir": frames_dir}
#     yield {"frames": frames}
#     ds_fps = mod_criteria.orig_frame_count_ds / mod_criteria.orig_loop_duration
#     ds_delay = 1 / ds_fps
#     create_criteria = CreationCriteria({
#         'fps': ds_fps,
#         'delay': ds_delay,
#         'format': mod_criteria.format,
#         'is_reversed': mod_criteria.is_reversed,
#         'is_transparent': True,
#         'flip_x': False, # Flipping horizontally is handled by gifsicle
#         'flip_y': False, # Flipping vertically is handled by gifsicle
#         'width': mod_criteria.width,
#         'height': mod_criteria.height,
#         'loop_count': mod_criteria.loop_count
#     })
#     new_image_path = yield from create_aimg(frames, out_dir, os.path.basename(img_path), create_criteria)
#     return new_image_path


def modify_aimg(img_path: str, out_dir: str, criteria: ModificationCriteria):
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
    sicle_args = gifsicle_args(criteria)
    magick_args = imagemagick_args(criteria)
    aopt_args = apngopt_args(criteria)
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
            target_path = yield from rebuild_aimg(target_path, out_dir, criteria)
            if aopt_args:
                target_path = yield from _apngopt_modify(aopt_args, target_path, out_full_path, total_ops, len(sicle_args) + len(magick_args))
        elif criteria.format == "GIF":
            yield {"msg": f"Changing format ({criteria.orig_format} -> {criteria.format})"}
            target_path = yield from rebuild_aimg(target_path, out_dir, criteria)
            out_full_path = str(target_path)
            if sicle_args:
                target_path = yield from _gifsicle_modify(sicle_args, target_path, out_full_path, total_ops)
            if magick_args:
                target_path = yield from _imagemagick_modify(magick_args, target_path, out_full_path, total_ops, len(sicle_args))             
            # yield {"preview_path": target_path}
    else:
        if criteria.orig_format == "GIF":
            if criteria.is_reversed or criteria.must_flip() or criteria.rotation:
                target_path = yield from rebuild_aimg(target_path, out_dir, criteria)
            if sicle_args:
                target_path = yield from _gifsicle_modify(sicle_args, target_path, orig_out_full_path, total_ops)
            if magick_args:
                target_path = yield from _imagemagick_modify(magick_args, target_path, orig_out_full_path, total_ops, len(sicle_args))
            # yield {"preview_path": target_path}
        elif criteria.orig_format == "PNG":
            if criteria.has_general_alterations() or criteria.rotation:
                target_path = yield from rebuild_aimg(target_path, out_dir, criteria)
            if aopt_args:
                target_path = yield from _apngopt_modify(aopt_args, target_path, out_full_path, total_ops, len(sicle_args) + len(magick_args))
    yield {"preview_path": target_path}

    yield {"CONTROL": "MOD_FINISH"}
