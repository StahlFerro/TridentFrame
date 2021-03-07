import os
import platform
import io
import string
import shutil
import shlex
import math
import time
import subprocess
import tempfile
import json
from collections import deque
from random import choices
from pprint import pprint
from typing import List, Dict, Tuple, Generator, Iterator
from pathlib import Path
from datetime import datetime

from PIL import Image
from apng import APNG, PNG

from .core_funcs import logger
from .core_funcs.config import (
    IMG_EXTS,
    ANIMATED_IMG_EXTS,
    STATIC_IMG_EXTS,
    get_absolute_cache_path,
    imager_exec_path,
)
from .core_funcs.criterion import (
    CreationCriteria,
    GIFOptimizationCriteria,
    APNGOptimizationCriteria,
    CriteriaBundle,
)
from .core_funcs.utility import _mk_temp_dir, shout_indices, shift_image_sequence
from .bin_funcs.imager_api import GifsicleAPI, APNGOptAPI, PNGQuantAPI


def _create_gifragments(image_paths: List[Path], criteria: CreationCriteria):
    """Generate a sequence of static GIF images created from the input sequence with the specified criteria.

    Args:
        image_paths (List[Path]): List of image paths to be converted into GIF images.
        out_path (Path): Output directory of the GIF sequences.
        criteria (CreationCriteria): Creation criteria.
    """
    # disposal = 0
    # if criteria.reverse:
    #     image_paths.reverse()
    # temp_gifs = []
    out_dir = _mk_temp_dir(prefix_name="tmp_gifrags")
    fcount = len(image_paths)
    logger.message(f"Criteria start frame {criteria.start_frame}")
    if criteria.start_frame:
        image_paths = shift_image_sequence(image_paths, criteria.start_frame)
    shout_nums = shout_indices(fcount, 1)
    for index, ipath in enumerate(image_paths):
        if shout_nums.get(index):
            logger.message(f"Processing frames... ({shout_nums.get(index)})")
        with Image.open(ipath) as im:
            im: Image.Image
            transparency = im.info.get("transparency", False)
            orig_width, orig_height = im.size
            alpha = None
            if criteria.flip_x:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            if criteria.flip_y:
                im = im.transpose(Image.FLIP_TOP_BOTTOM)
            if criteria.must_resize(orig_width, orig_height):
                resize_method_enum = getattr(Image, criteria.resize_method)
                # yield {"resize_method_enum": resize_method_enum}
                im = im.resize(
                    (round(criteria.resize_width), round(criteria.resize_height)),
                    resample=resize_method_enum,
                )
            if criteria.must_rotate():
                im = im.rotate(criteria.rotation, expand=True)
            fragment_name = os.path.splitext(f"{str.zfill(str(index), 6)}_{os.path.basename(ipath)}")[0]
            if criteria.reverse:
                reverse_index = len(image_paths) - (index + 1)
                fragment_name = f"rev_{str.zfill(str(reverse_index), 3)}_{fragment_name}"
            save_path = out_dir.joinpath(f"{fragment_name}.gif")
            if im.mode == "RGBA":
                if criteria.preserve_alpha:
                    alpha = im.getchannel("A")
                    im = im.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
                    mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                    im.paste(255, mask)
                    im.info["transparency"] = 255
                else:
                    black_bg = Image.new("RGBA", size=im.size)
                    black_bg.alpha_composite(im)
                    # im.show()
                    im = black_bg
                    # black_bg.show()
                    im = im.convert("P", palette=Image.ADAPTIVE)
                im.save(save_path)
            elif im.mode == "RGB":
                im = im.convert("RGB").convert("P", palette=Image.ADAPTIVE)
                im.save(save_path)
            elif im.mode == "P":
                if transparency:
                    if type(transparency) is int:
                        im.save(save_path, transparency=transparency)
                    else:
                        im = im.convert("RGBA")
                        alpha = im.getchannel("A")
                        im = im.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
                        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
                        im.paste(255, mask)
                        im.info["transparency"] = 255
                        im.save(save_path)
                else:
                    im.save(save_path)
            # yield {"msg": f"Save path: {save_path}"}
            # if absolute_paths:
            # temp_gifs.append(save_path)
            # else:
            # temp_gifs.append(os.path.relpath(save_path, os.getcwd()))
    return out_dir


def _build_gif(image_paths: List, out_full_path: Path, crbundle: CriteriaBundle) -> Path:
    """Generate an animated GIF iamge by first applying transformations and lossy compression on them (if specified) and then converting them
    into singular static GIF images, before compiled by Gifsicle.

    Args:
        image_paths (List): List of path to each image in a sequence
        out_full_path (Path): Complete output path with the target name of the GIF.
        crbundle (CriteriaBundle): Bundle of animated image creation criteria to adhere to.

    Returns:
        Path: Path of the created GIF.
    """
    gifragment_dir = _create_gifragments(image_paths, crbundle.create_aimg_criteria)
    out_full_path = GifsicleAPI.combine_gif_images(gifragment_dir, out_full_path, crbundle)
    logger.preview_path(out_full_path)
    logger.control("CRT_FINISH")
    return out_full_path


def _build_apng(image_paths: List[Path], out_full_path: Path, crbundle: CriteriaBundle) -> APNG:
    criteria = crbundle.create_aimg_criteria
    aopt_criteria = crbundle.apng_opt_criteria
    # temp_dirs = []

    if aopt_criteria.is_lossy:
        # qtemp_dir = _mk_temp_dir(prefix_name="quant_temp")
        # temp_dirs.append(qtemp_dir)
        image_paths = PNGQuantAPI.quantize_png_images(aopt_criteria, image_paths)

    if criteria.reverse:
        image_paths.reverse()

    apng = APNG()
    img_sizes = set(Image.open(i).size for i in image_paths)
    logger.message([f"({i[0]}, {i[1]})" for i in img_sizes])
    uneven_sizes = len(img_sizes) > 1 or (criteria.width, criteria.height) not in img_sizes

    shout_nums = shout_indices(len(image_paths), 1)
    if criteria.flip_x or criteria.flip_y or uneven_sizes or criteria.rotation:
        for index, ipath in enumerate(image_paths):
            if shout_nums.get(index):
                logger.message(f"Processing frames... ({shout_nums.get(index)})")
            with io.BytesIO() as bytebox:
                with Image.open(ipath) as im:
                    im: Image.Image
                    orig_width, orig_height = im.size
                    if criteria.must_resize(orig_width, orig_height):
                        resize_method_enum = getattr(Image, criteria.resize_method)
                        # yield {"resize_method_enum": resize_method_enum}
                        im = im.resize(
                            (round(criteria.width), round(criteria.height)),
                            resize_method_enum,
                        )
                    if criteria.flip_x:
                        im = im.transpose(Image.FLIP_LEFT_RIGHT)
                    if criteria.flip_y:
                        im = im.transpose(Image.FLIP_TOP_BOTTOM)
                    if criteria.rotation:
                        im = im.rotate(criteria.rotation, expand=True)
                    im.save(bytebox, "PNG")
                apng.append(PNG.from_bytes(bytebox.getvalue()), delay=int(criteria.delay * 1000))
        logger.message("Saving APNG....")
        apng.num_plays = criteria.loop_count
        apng.save(out_full_path)
    else:
        logger.message("Saving APNG....")
        apng = APNG.from_files(image_paths, delay=int(criteria.delay * 1000))
        apng.num_plays = criteria.loop_count
        apng.save(out_full_path)

    if aopt_criteria.is_optimized:
        out_full_path = APNGOptAPI.optimize_apng(out_full_path, out_full_path, aopt_criteria)

    # for td in temp_dirs:
    #     shutil.rmtree(td)
    logger.preview_path(out_full_path)
    logger.control("CRT_FINISH")

    return out_full_path


def create_aimg(image_paths: List[Path], out_dir: Path, filename: str, crbundle: CriteriaBundle):
    """ Umbrella generator for creating animated images from a sequence of images """
    # abs_image_paths = [os.path.abspath(ip) for ip in image_paths if os.path.exists(ip)]
    img_paths = [f for f in image_paths if str.lower(f.suffix[1:]) in STATIC_IMG_EXTS]
    # workpath = os.path.dirname(img_paths[0])
    # Test if inputted filename has extension, then remove it from the filename
    img_format = crbundle.create_aimg_criteria.extension
    if len(img_paths) < 2:
        raise Exception(f"At least 2 images is needed for an animated {img_format}!")
    fname, ext = os.path.splitext(filename)
    if ext:
        filename = fname
    # if not out_dir:
    #     raise Exception("No output folder selected, please select it first")
    # out_dir = os.path.abspath(out_dir)
    # if not os.path.exists(out_dir):
    #     raise Exception(f"The specified absolute out_dir does not exist!\n{out_dir}")
    if img_format == "GIF":
        out_full_path = out_dir.joinpath(f"{filename}.gif")
        filename = f"{filename}.gif"
        return _build_gif(img_paths, out_full_path, crbundle)

    elif img_format == "PNG":
        out_full_path = out_dir.joinpath(f"{filename}.png")
        return _build_apng(img_paths, out_full_path, crbundle)
